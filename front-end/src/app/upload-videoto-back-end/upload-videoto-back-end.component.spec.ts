import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadVideotoBackEndComponent } from './upload-videoto-back-end.component';

describe('UploadVideotoBackEndComponent', () => {
  let component: UploadVideotoBackEndComponent;
  let fixture: ComponentFixture<UploadVideotoBackEndComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UploadVideotoBackEndComponent]
    });
    fixture = TestBed.createComponent(UploadVideotoBackEndComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
