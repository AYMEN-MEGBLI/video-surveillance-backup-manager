import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './main/main.component';
import { SettingComponent } from './setting/setting.component';
import { VideoStreamComponent } from './video-stream/video-stream.component';
import { InvalidPageComponent } from './invalid-page/invalid-page.component';
const routes: Routes = [
  {path:"",component:MainComponent},
  {path : "detection-from-Video",loadChildren: () => import("./detection-from-video/detection-from-video.module").then(m => m.DetectionFromVideoModule)},
  {path: 'video', loadChildren: () => import("./video-playlist-gallery/video-playlist-gallery.module").then(m => m.VideoPlaylistGalleryModule)},
  {path: 'settings', component:SettingComponent},
  {path: 'video-stream', component:VideoStreamComponent},
  {path:"**",component:InvalidPageComponent}
  
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
