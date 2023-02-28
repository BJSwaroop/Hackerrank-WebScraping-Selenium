import { Injectable } from "@angular/core";
import { HttpInterceptor, HttpHandler, HttpRequest, HttpEvent } from "@angular/common/http";
import { Observable } from "rxjs";
@Injectable()

export class Interceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    
    
    const customReq = request.clone({
        setHeaders :{
            'Authorization': "Basic " + window.btoa('admin:Swaroop@143'),
        }
    
    });
    return next.handle(customReq);
  }
}