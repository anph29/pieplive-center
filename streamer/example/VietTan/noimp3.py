# import pydub
import subprocess as sp
# song = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1.mp3")
# song1 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+02+Ly+Con+Sao+1512.mp3", "mp3")
# song2 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+03+Ly+Cay+Da+1512.mp3", "mp3")
# song3 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+04+La+1512.mp3", "mp3")
# song4 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+05+Thang+Bom+1212.mp3", "mp3")
# song5 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+06+Dem+Nghe+Mua+mua+1612.mp3", "mp3")
# song6 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+07+Ben+Bo+25+12.mp3", "mp3")
# song7 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+08+Toi+ru+em+ngu+25+12.mp3", "mp3")
# song8 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+09+xua+1512.mp3", "mp3")
# song9 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+10+Some+Thing+1512.mp3", "mp3")
# song10 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+11+ABC+1212.mp3", "mp3")
# song11 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/1309025+-+1309025+-+12+12.mp3", "mp3")
# song3 = pydub.AudioSegment.from_mp3("C:/Users/Thong/Desktop/VietTan/.mp3", "mp3")

# combined = pydub.AudioSegment.empty()

# combined += song
# combined += song1
# combined += song2
# combined += song3
# combined += song4
# combined += song5
# combined += song6
# combined += song7
# combined += song8
# combined += song9
# combined += song10
# combined += song11

# combined.export("thong.mp3", format="mp3")

cam = "../../ffmpeg-win/ffmpeg.exe -i concat:1.mp3|2.mp3|3.mp3|4.mp3|5.mp3 -acodec copy Nhac-Khong-Loi.mp3 -map_metadata 0:1"
self.pipe = sp.Popen(cam)