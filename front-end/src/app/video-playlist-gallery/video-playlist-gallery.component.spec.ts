import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoPlaylistGalleryComponent } from './video-playlist-gallery.component';

describe('VideoPlaylistGalleryComponent', () => {
  let component: VideoPlaylistGalleryComponent;
  let fixture: ComponentFixture<VideoPlaylistGalleryComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VideoPlaylistGalleryComponent]
    });
    fixture = TestBed.createComponent(VideoPlaylistGalleryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
