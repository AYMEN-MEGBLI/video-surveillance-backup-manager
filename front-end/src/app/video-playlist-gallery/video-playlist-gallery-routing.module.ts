import { Component, NgModule, OnInit } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VideoPlaylistGalleryComponent } from './video-playlist-gallery.component';

const routes: Routes = [
  {path:"" , component: VideoPlaylistGalleryComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class VideoPlaylistGalleryRoutingModule  {

 }
