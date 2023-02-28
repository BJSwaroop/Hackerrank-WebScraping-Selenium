import { TestBed } from '@angular/core/testing';

import { ContentServiceService } from './content-service.service';

describe('ContentServiceService', () => {
  let service: ContentServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ContentServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
