import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProductApiService } from '../../services/product.api.service';
import { ProductModel } from '../../models/product.model';

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.html',
  styleUrl: './product-details.css',
})
export class ProductDetails {

  product = signal<ProductModel | null>(null);

  private route = inject(ActivatedRoute);
  private productService = inject(ProductApiService);

  ngOnInit() {

    const id = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.productService.getProductById(id).subscribe({
      next: (response: any) => {
        this.product.set(response);
      },
      error: (error) => {
        console.error('Failed to fetch product', error);
      },
    });

  }
}