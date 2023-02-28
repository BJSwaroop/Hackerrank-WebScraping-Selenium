import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsersAttemptsComponent } from './users-attempts.component';

describe('UsersAttemptsComponent', () => {
  let component: UsersAttemptsComponent;
  let fixture: ComponentFixture<UsersAttemptsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UsersAttemptsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UsersAttemptsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
