import bluetooth
import xml.etree.ElementTree as ET

uuid = "8b6814d3-6ce7-4498-9700-9312c1711f63"
request_header_len = 3
response_header_len = 7

#BELOW IS ACTUALLY A GET
#/api/appli_version/set?arg=1.2
account_user        = '/api/account/username'
equalizer           = '/api/audio/equalizer/enabled'
noise_cancellation  = '/api/audio/noise_cancellation/enabled'
noise_control       = '/api/audio/noise_control'
### with noise control, type="aoc" means 'Street Mode'
###                     type="anc" means 'Noise Cancelling'
sound_effect        = '/api/audio/sound_effect' #/enabled'
bypass_preset       = '/api/audio/preset/bypass'
preset_counter      = '/api/audio/preset/counter'
preset_current      = '/api/audio/preset/current'
smart_audio_tune    = '/api/audio/smart_audio_tune'
thumb_equalizer     = '/api/audio/thumb_equalizer/value'
track_data          = '/api/audio/track/metadata'
bt_friendly_name    = '/api/bluetooth/friendlyname'
flight_mode         = '/api/flight_mode'
text_to_speech      = '/api/software/tts'
firmware_version    = '/api/software/version'
anc_phone_mode      = '/api/system/anc_phone_mode/enabled'
auto_connect        = '/api/system/auto_connection/enabled'
auto_power_off      = '/api/system/auto_power_off'
battery             = '/api/system/battery'
bt_address          = '/api/system/bt_address'
color               = '/api/system/color'
device_type         = '/api/system/device_type'
pi                  = '/api/system/pi'
head_detection      = '/api/system/head_detection/enabled'

#Exists, but no content in answer
#sound_effect = audio_path + 'specific_mode/enabled'
target_address = None

parrot_fr_devices = bluetooth.find_service( uuid = uuid, address = "A0:14:3D:1F:5C:C7" )

def getGetBody(valueToGet):
    return 'GET ' + valueToGet + '/get'

def makeGetRequest(requestText):
    requestBody = getGetBody(requestText).encode()
    requestLength = (len(requestBody)+request_header_len).to_bytes(1, byteorder='big')
    message = b'\x00' + requestLength  + b'\x80' + requestBody
    sock.send(message)
    resp = sock.recv(response_header_len)
    response_length = resp[1]
    data = sock.recv(response_length-response_header_len)
    answer = ET.fromstring(data)
    if answer.get("error") == "true":
        raise Error("Received an error from Parrot: %r" % (data))
    return answer

for device in parrot_fr_devices:
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect( (device['host'], device['port']) )
    sock.send(b'\x00\x03\x00')
    data = sock.recv(1024)
    resp = makeGetRequest(account_user)
    print ( resp.find('account').get('username'))
    resp = makeGetRequest(equalizer)
    print ( resp.find('audio/equalizer').get('enabled'))
    resp = makeGetRequest(noise_cancellation)
    print ( resp.find('audio/noise_cancellation').get('enabled'))
    resp = makeGetRequest(noise_control)
    print ( resp.find('audio/noise_control').get('type'), resp.find('audio/noise_control').get('value'))
    resp = makeGetRequest(sound_effect)
    print ( resp.find('audio/sound_effect').get('enabled'), resp.find('audio/sound_effect').get('room_size'), resp.find('audio/sound_effect').get('angle')) 
    resp = makeGetRequest(bypass_preset)
    print ( resp.find('audio/preset').get('bypass'))
    resp = makeGetRequest(preset_counter)
    print ( resp.find('audio/preset').get('counter'))
    resp = makeGetRequest(preset_current)
    print ( resp.find('audio/preset').get('id'))
    resp = makeGetRequest(smart_audio_tune)
    print ( resp.find('audio/smart_audio_tune').get('enabled'))
    resp = makeGetRequest(thumb_equalizer)
    print ( resp.find('audio/thumb_equalizer').get('r'), resp.find('audio/thumb_equalizer').get('theta'))
    resp = makeGetRequest(track_data)
    print ( resp.find('audio/track/metadata').get('playing'), resp.find('audio/track/metadata').get('title'), resp.find('audio/track/metadata').get('artist'), resp.find('audio/track/metadata').get('album'), resp.find('audio/track/metadata').get('genre')) 
    resp = makeGetRequest(bt_friendly_name)
    print ( resp.find('bluetooth').get('friendlyname'))
    resp = makeGetRequest(flight_mode)
    print ( resp.find('flight_mode').get('enabled'))
    resp = makeGetRequest(text_to_speech)
    print ( resp.find('tts').get('enabled'))
    resp = makeGetRequest(firmware_version)
    print ( resp.find('software').get('sip6'), resp.find('software').get('pic'), resp.find('software').get('tts'))
    resp = makeGetRequest(anc_phone_mode)
    print ( resp.find('system/anc_phone_mode').get('enabled'))
    resp = makeGetRequest(auto_connect)
    print ( resp.find('system/auto_connection').get('enabled'))
    resp = makeGetRequest(auto_power_off)
    print ( resp.find('system/auto_power_off').get('value'))
    resp = makeGetRequest(battery)
    print ( resp.find('system/battery').get('percent'))
    resp = makeGetRequest(bt_address)
    print ( resp.find('system/bt_address').get('value').upper())
    resp = makeGetRequest(color)
    print ( resp.find('system/color').get('value'))
    resp = makeGetRequest(device_type)
    print ( resp.find('system/device_type').get('value'))
    resp = makeGetRequest(pi)
    print ( resp.find('system').get('pi'))
    resp = makeGetRequest(head_detection)
    print ( resp.find('system/head_detection').get('enabled') )
    sock.close()
    break
