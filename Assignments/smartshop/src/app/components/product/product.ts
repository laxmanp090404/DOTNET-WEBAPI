import { Component, input } from '@angular/core';
import { ProductModel } from '../../models/product.model';

@Component({
  selector: 'app-product',
  templateUrl: './product.html',
  styleUrl: './product.css',
})
export class Product {
  product = input.required<ProductModel>();
}