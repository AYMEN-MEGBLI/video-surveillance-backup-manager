import { Component, ElementRef, Input, OnInit, QueryList, ViewChildren } from '@angular/core';
import { VideoService } from '../services/video.service';

@Component({
  selector: 'app-video-playlist-gallery',
  templateUrl: './video-playlist-gallery.component.html',
  styleUrls: ['./video-playlist-gallery.component.scss']
})
export class VideoPlaylistGalleryComponent implements OnInit {
  @Input() motionData: any | null = null; // Default to null if not provided
  @ViewChildren('vid') vid!: QueryList<ElementRef>;
  main_vd: any = null; // Initialize as null
  videos: any[] = []; // Initialize as empty array

  constructor(private video_service: VideoService) { }

  ngOnInit() {
    this.get_videos_details();
  }

  get_videos_details() {
    this.video_service.get_videos_details().subscribe((data) => {
      console.log("data", data);
      this.videos = data["videos"] || []; // Safeguard if data["videos"] is undefined
      if (this.videos.length > 0) {
        this.main_vd = this.videos[0];
        this.motionData = this.videos[0].categorized_objects;
      }
    });
  }

  onSeek(position: number) {
    // Assuming you have a player object; otherwise, handle seek for the native video element
    const videoElement = document.querySelector('video') as HTMLVideoElement;
    if (videoElement) {
      videoElement.currentTime = position;
      videoElement.play();
    }
  }

  print() {
    this.vid.forEach((vid, index) => {
      console.log(`Video ${index}:`, vid.nativeElement);
    });
  }

  change_vd(i: number) {
    this.vid.forEach((vid) => { vid.nativeElement.classList.remove('active'); });
    this.vid.toArray()[i].nativeElement.classList.add('active');
    this.main_vd = this.videos[i];
    this.motionData = this.videos[i].categorized_objects;
    
    
  }

  get_vd_url(file_name: string): string {
    return `http://127.0.0.1:8000/video/${file_name}`;
  }
}
