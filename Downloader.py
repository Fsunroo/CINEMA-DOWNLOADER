from Crypto.Cipher import AES
import requests
import m3u8
import subprocess

def Get_master():
	master_url= input('master_url ra vared knid: ')
	print("")
	print("")
	print("")
	return master_url


def ChooseQuality(master_url):
	quality_list=master_url[master_url.index('h_')+3:master_url.index(',k.mp4')].split(',')
	quality_dict={}
	for item in quality_list : quality_dict[quality_list.index(item)]=item
	print(f'available qualities:{quality_dict}')
	print('')
	choice=input('choose your Option: ')
	# choice=1
	return int(choice)






master_url= Get_master()
# master_url= 'https://cinemamarket.arvanvod.com/QjwP8y9RbZ/54c6344540e974cec4b03908c94c673d/1587284900/KPjw3dyvqo/h_,144_128,360_400,480_500,720_1500,k.mp4.list/master.m3u8'

choice= ChooseQuality(master_url)
r=requests.get(master_url)
master_m3u8=m3u8.loads(r.text)
base_url= master_url.replace('master.m3u8','')

index_m3u8=master_m3u8.data['playlists'][choice]['uri']


r=requests.get(base_url+index_m3u8)

index_m3u8=m3u8.loads(r.text)

key_uri =index_m3u8.data['segments'][2]['key']['uri']
#data_uri= index_m3u8.data['segments'][2]['uri']

# data=requests.get(base_url+data_uri)
key=requests.get(base_url+key_uri).content




with open('Video.ts','wb') as f :
	for segment in index_m3u8.data['segments']:
		data_uri=segment['uri']
		data=requests.get(base_url+data_uri).content
		data_=data_uri.replace('seg-','')
		num=int(data_[:data_.index('-')])
		iv=num.to_bytes(16,'big')
		decryptor = AES.new(key, AES.MODE_CBC, IV=iv)
		decoded_data = decryptor.decrypt(data)
		f.write(decoded_data)
		print(num)
f.close()
#-----------------------------



aoudio_uri=master_m3u8.data['media'][0]['uri']
r=requests.get(base_url+aoudio_uri)

index_m3u8=m3u8.loads(r.text)

key_uri =index_m3u8.data['segments'][2]['key']['uri']
#data_uri= index_m3u8.data['segments'][2]['uri']

# data=requests.get(base_url+data_uri)
key=requests.get(base_url+key_uri).content




with open('Aoudio.ts','wb') as f :
	for segment in index_m3u8.data['segments']:
		data_uri=segment['uri']
		data=requests.get(base_url+data_uri).content
		data_=data_uri.replace('seg-','')
		num=int(data_[:data_.index('-')])
		iv=num.to_bytes(16,'big')
		decryptor = AES.new(key, AES.MODE_CBC, IV=iv)
		decoded_data = decryptor.decrypt(data)
		f.write(decoded_data)
		print(num)
f.close()

def combine_audio(vidname, audname, outname, fps=25):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

combine_audio('Video.ts','Aoudio.ts','output.mp4')
