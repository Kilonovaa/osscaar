from moviepy.editor import VideoFileClip

def compress_video(input_path, output_path, bitrate='1000k'):
    # Load the video clip
    clip = VideoFileClip(input_path)

    # Set the output file with a lower bitrate for compression
    compressed_clip = clip.resize(width=clip.size[0] // 1, height=clip.size[1] // 1)
    compressed_clip.write_videofile(output_path, bitrate=bitrate)

if __name__ == "__main__":
    # Specify your input and output file paths
    input_file = './orionnebula.mp4'
    output_file = './output_compressed.mp4'

    # Specify the desired bitrate for compression (adjust as needed)
    compression_bitrate = '25k'

    # Compress the video
    compress_video(input_file, output_file, bitrate=compression_bitrate)