import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HackerrankPlagiarismCheckComponent } from './hackerrank-plagiarism-check/hackerrank-plagiarism-check.component';
import { UsersAttemptsComponent } from './users-attempts/users-attempts.component';

const routes: Routes = [
  {path: '',component: HackerrankPlagiarismCheckComponent},
  {path: 'usersAttempts',component: UsersAttemptsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
