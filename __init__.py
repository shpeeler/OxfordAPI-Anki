from aqt import mw
from aqt.utils import showWarning
from anki.hooks import addHook
from anki.utils import stripHTMLMedia
from .request.requester import Requester 
from .request.util.util import Util
import urllib

# loading the configuration file
config = Util.read_config()
requester = Requester(app_id=config['app_id'], app_key=config['app_key'])

def get_word_data(editor):
    """
    starts the lookup session
    """


    # get word from current field
    word = stripHTMLMedia(editor.note.fields[editor.currentField])

    # request the word information and translation
    params = ['definitions', 'examples']
    information_json = requester.get_information(   word=word.lower(), 
                                                    language=config['src_language'],
                                                    params=params)

    translation_json = requester.get_translation(   word=word.lower(), 
                                                    src_language=config['src_language'], 
                                                    target_language=config['target_language'])

    definition = None
    example = None
    audio_url = None
    translation = None

    if information_json != None:
        # read information 
        definition = information_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        example = information_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text']
        audio_url = information_json['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
         
        # add audio to media library
        audio_file = save_audio(config['audio_directory'], word, audio_url)
        editor.addMedia(audio_file)
    else:
        showWarning('OxfordAPI: no information found for the word: {}'.format(word))


    # if translation_json != None:
    #     # read translation
    #     translation = translation_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['translations'][0]['text']
    # else:
    #     showWarning('OxfordAPI: no translation found for the word: {}'.format(word))

    # setting the field values
    for field in editor.note.keys():
        if field == config['definition'] and definition != None:
            editor.note[field] = str(definition)
        elif field == config['example'] and example != None:
            editor.note[field] = str("<i>'{}'</i>".format(example))
        elif field == config['translation'] and translation != None:
            editor.note[field] = str(translation)
        elif field == config['audio'] and audio_file != None:
            editor.note[field] = str('[sound:{}.{}]'.format(word, 'mp3'))

    # updating gui elements
    mw.reset()

def addEditorButton(buttons, editor):
    """
    creates a new button
    returns new set of buttons
    """

    editor._links['data'] = get_word_data
    baseDir = Util.get_base_directory()
    icon = baseDir + '/resources/arrow.png'

    return buttons + [editor._addButton(icon, 'data', 'lookup word data')]

def lookfor(json, key):
    """
    searches for the given key in given json
    returns the first result
    """

    result = Util.find(json, key)
    
    if result == None:
        return None

    while(type(result) is dict) or (type(result) is list):    
        if type(result) is dict:
            result = result['text']
        if type(result) is list:
            result = result[0]

    return result

def save_audio(directory, word, audio_url):
    """
    downloads the audio file and saves it to the configured directory
    returns the filepath
    """

    file_data = urllib.request.urlopen(audio_url)
    audio = file_data.read()

    filename = '{0}/{1}.{2}'.format(directory, word, 'mp3')
    with open(filename, 'wb') as f:
        f.write(audio)

    return filename

addHook('setupEditorButtons', addEditorButton)