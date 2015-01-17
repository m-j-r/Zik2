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
noise_control_enabled = '/api/audio/noise_control/enabled'
noise_control       = '/api/audio/noise_control'
### with noise control, type="aoc" means 'Street Mode'
###                     type="anc" means 'Noise Cancelling'
sound_effect        = '/api/audio/sound_effect' #/enabled'
sound_effect_enabled= '/api/audio/sound_effect/enabled'
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
""" 
GET /api/audio/sound_effect/enabled/set?arg=true
GET /api/audio/sound_effect/enabled/set?arg=false
GET /api/audio/equalizer/enabled/set?arg=true
GET /api/audio/equalizer/enabled/set?arg=false
GET /api/audio/noise_control/enabled/set?arg=false
GET /api/audio/noise_control/enabled/set?arg=true
GET /api/audio/noise_control/set?arg=anc&value=2
GET /api/audio/noise_control/set?arg=anc&value=1

GET /api/audio/noise_control/set?arg=off&value=0
<?xml version="1.0" encoding="UTF-8"?><answer path="/api/audio/noise_control/set?arg"><notify path="/api/audio/noise_control/enabled/get"/></answer>
GET /api/audio/noise_control/enabled/get
<?xml version="1.0" encoding="UTF-8"?><answer path="/api/audio/noise_control/enabled/get"><audio><noise_control enabled="false"/></audio></answer>

GET /api/audio/noise_control/set?arg=aoc&value=1
GET /api/audio/noise_control/set?arg=aoc&value=2
GET /api/audio/thumb_equalizer/value/set?arg=-2.5,2.5,5.5,5.0,4.0
GET /api/audio/thumb_equalizer/value/set?arg=1.0,3.5,2.5,2.0,0.5
GET /api/audio/sound_effect/room_size/set?arg=living
GET /api/audio/sound_effect/room_size/set?arg=jazz
GET /api/audio/sound_effect/room_size/set?arg=concert
GET /api/audio/sound_effect/room_size/set?arg=silent
GET /api/audio/sound_effect/angle/set?arg=30
GET /api/audio/sound_effect/angle/set?arg=60
GET /api/audio/sound_effect/angle/set?arg=90
GET /api/audio/sound_effect/angle/set?arg=120
GET /api/audio/sound_effect/angle/set?arg=150
GET /api/audio/sound_effect/angle/set?arg=180
GET /api/system/head_detection/enabled/set?arg=false
GET /api/system/head_detection/enabled/set?arg=true
GET /api/system/auto_connection/enabled/set?arg=false
GET /api/system/auto_connection/enabled/set?arg=true
GET /api/bluetooth/friendlyname/set?arg=MJR headphones
"""

#Exists, but no content in answer
#sound_effect = audio_path + 'specific_mode/enabled'
target_address = None

parrot_fr_devices = bluetooth.find_service( uuid = uuid, address = "A0:14:3D:1F:5C:C7" )

def makeGetRequest(valueToGet):
    return makeRequest(('GET ' + valueToGet + '/get').encode())

def makeSetRequest(valueToSet, value):
    return makeRequest(('GET ' + valueToSet + '/set?arg=' + value).encode())

def makeRequest(requestBody):
    requestLength = (len(requestBody)+request_header_len).to_bytes(1, byteorder='big')
    sock.send(b'\x00' + requestLength  + b'\x80' + requestBody)
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

    ### USERNAME
    resp = makeGetRequest(account_user)
    parrot_username = resp.find('account').get('username')

    ### EQUALIZER
    resp = makeGetRequest(equalizer)
    eq_enabled = resp.find('audio/equalizer').get('enabled')

    resp = makeGetRequest(thumb_equalizer)
    te_r_value = resp.find('audio/thumb_equalizer').get('r')
    te_theta = resp.find('audio/thumb_equalizer').get('theta')

    ### ANC INFO
    resp = makeGetRequest(noise_cancellation)
    nc_enabled = resp.find('audio/noise_cancellation').get('enabled')

    resp = makeGetRequest(noise_control_enabled)
    nc_enabled = resp.find('audio/noise_control').get('enabled')
    resp = makeGetRequest(noise_control)
    nc_type = resp.find('audio/noise_control').get('type')
    nc_value = resp.find('audio/noise_control').get('value')
    resp = makeGetRequest(anc_phone_mode)
    nc_phone = resp.find('system/anc_phone_mode').get('enabled')

    ### SOUND EFFECT
    resp = makeGetRequest(sound_effect)
    se_enabled = resp.find('audio/sound_effect').get('enabled')
    se_room_size = resp.find('audio/sound_effect').get('room_size')
    se_angle = resp.find('audio/sound_effect').get('angle') 

    ### PRESET INFO
    resp = makeGetRequest(bypass_preset)
    pre_bypass = resp.find('audio/preset').get('bypass')

    resp = makeGetRequest(preset_counter)
    pre_counter = resp.find('audio/preset').get('counter')

    resp = makeGetRequest(preset_current)
    pre_current = resp.find('audio/preset').get('id')

    ### TRACK
    resp = makeGetRequest(track_data)
    track_playing = resp.find('audio/track/metadata').get('playing')
    track_title = resp.find('audio/track/metadata').get('title')
    track_artist = resp.find('audio/track/metadata').get('artist')
    track_album = resp.find('audio/track/metadata').get('album')
    track_genre = resp.find('audio/track/metadata').get('genre') 

    ### BLUETOOTH INFO
    resp = makeGetRequest(bt_friendly_name)
    bt_name = resp.find('bluetooth').get('friendlyname')

    resp = makeGetRequest(bt_address)
    bt_addr = resp.find('system/bt_address').get('value').upper()

    ### TEXT_TO_SPEECH
    resp = makeGetRequest(text_to_speech)
    tts_enabled = resp.find('tts').get('enabled')

    resp = makeGetRequest(firmware_version)
    tts_lang = resp.find('software').get('tts')

    ### FIRMWARE
    fw_version = resp.find('software').get('sip6')
    fw_pic = resp.find('software').get('pic')

    ### BATTERY INFO
    resp = makeGetRequest(battery)
    bat_level = resp.find('system/battery').get('percent')
    bat_state = resp.find('system/battery').get('state')

    ### DEVICE INFO
    resp = makeGetRequest(color)
    dev_color = resp.find('system/color').get('value')

    resp = makeGetRequest(device_type)
    dev_type = resp.find('system/device_type').get('value')

    resp = makeGetRequest(pi)
    dev_pi = resp.find('system').get('pi')

    ### FLAGS
    resp = makeGetRequest(head_detection)
    head_detect_enabled = resp.find('system/head_detection').get('enabled')

    resp = makeGetRequest(auto_connect)
    ac_enabled = resp.find('system/auto_connection').get('enabled')

    resp = makeGetRequest(auto_power_off)
    auto_off_duration = resp.find('system/auto_power_off').get('value')

    resp = makeGetRequest(flight_mode)
    fm_enabled = resp.find('flight_mode').get('enabled')

    resp = makeGetRequest(smart_audio_tune)
    sat_enabled = resp.find('audio/smart_audio_tune').get('enabled')

    print ( 'username: ', parrot_username )
    print ( 'equalizer is enabled: ', eq_enabled )
    print ( 'noise cancellation:', '\n enabled:', nc_enabled, '\n type:', nc_type, '\n value:', nc_value, '\n ANC Phone Mode:', nc_phone)
    print ( 'sound effect: \n', 'enabled:', se_enabled, '\n', 'room_size:', se_room_size, '\n', 'angle:', se_angle) 
    print ( 'preset:', '\n bypassed', pre_bypass, '\n counter:', pre_counter, '\n current:', pre_current)
    #print ( 'Device:', '\n Auto Connect:', dev_ac, '\n Auto Power Off:', dev_auto_off, '\n Battery level:', dev_battery, '\n MAC address:', dev_bt_addr, '\n Color:', dev_color, '\n Type:', dev_type, '\n PI:', dev_pi) 
    print ( 'battery: ', bat_level, '% ,', bat_state )
    sock.close()
    break

