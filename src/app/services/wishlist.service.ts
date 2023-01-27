import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WishlistService {
  private apiUrl = 'http://localhost:5000/wishlist';

  constructor(private http: HttpClient) { }

  getWishlistItems(): Observable<Array<any>> {
    return this.http.get<Array<any>>(this.apiUrl).pipe(
      map(data => Array.from(data))
    );
  }
}
