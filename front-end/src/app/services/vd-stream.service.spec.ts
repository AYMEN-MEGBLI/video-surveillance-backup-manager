import { TestBed } from '@angular/core/testing';

import { VdStreamService } from './vd-stream.service';

describe('VdStreamService', () => {
  let service: VdStreamService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VdStreamService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
