import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DetectionFromVideoComponent } from './detection-from-video.component';
const routes: Routes = [
  {path:"",component:DetectionFromVideoComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DetectionFromVideoRoutingModule { }
