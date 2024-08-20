import { Component } from '@angular/core';

@Component({
  selector: 'app-setting',
  templateUrl: './setting.component.html',
  styleUrls: ['./setting.component.scss']
})
export class SettingComponent {
 // Variables for storing settings and progress
 storageUsed: number = 75; // Example storage used percentage
 recordMotion: boolean = true;
 recordHuman: boolean = false;
 recordVehicle: boolean = false;
 recordAnimals: boolean = false;

 // Method to format storage
 formatStorage() {
   if (confirm("Êtes-vous sûr de vouloir formater le stockage?")) {
     // Logic to format storage goes here
     console.log("Stockage formaté.");
   }
 }

 // Method to delete videos
 deleteVideos() {
   if (confirm("Êtes-vous sûr de vouloir supprimer toutes les vidéos?")) {
     // Logic to delete videos goes here
     console.log("Vidéos supprimées.");
   }
 }
}
