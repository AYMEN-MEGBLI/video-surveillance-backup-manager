import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetectionFromVideoComponent } from './detection-from-video.component';

describe('DetectionFromVideoComponent', () => {
  let component: DetectionFromVideoComponent;
  let fixture: ComponentFixture<DetectionFromVideoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DetectionFromVideoComponent]
    });
    fixture = TestBed.createComponent(DetectionFromVideoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
