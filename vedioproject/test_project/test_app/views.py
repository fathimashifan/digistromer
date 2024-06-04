import os
import subprocess
from django.shortcuts import render, redirect
from .forms import VedioGalleryForm
from .models import VedioGallery
from django.shortcuts import render, get_object_or_404

def upload_video(request):
    form = VedioGalleryForm()

    if request.method == 'POST':
        form = VedioGalleryForm(request.POST, request.FILES)

        if form.is_valid():
            video_instance = form.save(commit=False)
            video_instance.save()

            # Path to the uploaded MP4 video
            mp4_path = video_instance.vedio_material.path

            # Define the output path for the MPD file and segments
            base, ext = os.path.splitext(mp4_path)
            mpd_path = base + '.mpd'

            # Use ffmpeg to convert MP4 to MPD (DASH format)
            command = [
               'ffmpeg', '-i', mp4_path,
    '-c', 'copy', '-map', '0',
    '-f', 'dash', mpd_path
            ]

            try:
                subprocess.run(command, check=True, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode()
                # Log the error message or handle it as needed
                print(f'ffmpeg error: {error_message}')
                return render(request, 'upload_video.html', {'form': form, 'videos': VedioGallery.objects.all(), 'error': error_message})

            # Save the MPD file path in the video_instance
            video_instance.vedio_material.name = os.path.basename(mpd_path)
            video_instance.save()

            # Optionally, remove the temporary MP4 file
            os.remove(mp4_path)

            return redirect('upload_video')

    videos = VedioGallery.objects.all()
 
    return render(request, 'upload_video.html', {'form': form, 'videos': videos,})
