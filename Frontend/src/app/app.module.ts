import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HackerrankPlagiarismCheckComponent } from './hackerrank-plagiarism-check/hackerrank-plagiarism-check.component';
import { FormsModule , ReactiveFormsModule} from '@angular/forms';
import { Interceptor } from './interceptor';

@NgModule({
  declarations: [
    AppComponent,
    HackerrankPlagiarismCheckComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [
    
    { provide: HTTP_INTERCEPTORS, useClass: Interceptor, multi: true }  
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
