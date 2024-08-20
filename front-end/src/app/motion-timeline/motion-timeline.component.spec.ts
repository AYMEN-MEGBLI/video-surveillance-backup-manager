import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MotionTimelineComponent } from './motion-timeline.component';

describe('MotionTimelineComponent', () => {
  let component: MotionTimelineComponent;
  let fixture: ComponentFixture<MotionTimelineComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MotionTimelineComponent]
    });
    fixture = TestBed.createComponent(MotionTimelineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
