import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HackerrankPlagiarismCheckComponent } from './hackerrank-plagiarism-check.component';

describe('HackerrankPlagiarismCheckComponent', () => {
  let component: HackerrankPlagiarismCheckComponent;
  let fixture: ComponentFixture<HackerrankPlagiarismCheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HackerrankPlagiarismCheckComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HackerrankPlagiarismCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
