import { Component, OnInit } from '@angular/core';
import { WishlistService } from '../../services/wishlist.service';

@Component({
  selector: 'app-wishlist',
	template: `
    <div class="card-body" *ngFor="let item of wishlistItems">
    <h1 class="card-title pricing-card-title">{{ item.price }}<small class="text-muted fw-light">$CAD</small></h1>
    <ul class="list-unstyled mt-3 mb-4"  >
      <li> {{ item.name }} -  </li>

    </ul>
    <button type="button" class="w-100 btn btn-lg btn-primary">Contact us</button>
  </div>
  `,
  styles: []
})
export class WishlistComponent implements OnInit {
  wishlistItems: { name: string, price: number }[] = [];

  constructor(private wishlistService: WishlistService) { }

  ngOnInit() {
    this.wishlistService.getWishlistItems().subscribe(
		data => {
			this.wishlistItems = data;
      }
    );
  }
}

