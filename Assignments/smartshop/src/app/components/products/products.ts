import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { ProductModel } from '../../models/product.model';
import { ProductApiService } from '../../services/product.api.service';
import { Product } from '../product/product';

@Component({
  selector: 'app-products',
  imports: [Product],
  templateUrl: './products.html',
  styleUrl: './products.css',
})
export class Products {

  products = signal<ProductModel[]>([]);

  constructor(
    private productService: ProductApiService,
    private router: Router
  ) {

    this.productService.getProducts().subscribe({
      next: (response: any) => {
        this.products.set(response.products);
      },
      error: (error: any) => {
        console.error('Failed to fetch products', error);
      },
    });
  }

  onProductClick(productId: number) {
    this.router.navigate(['/products', productId]);
  }
}