# Smartshop
## Outputs
- Ouput screenshots on [Outputs](./Output/)
## Project Tree

```text
smartshop/
└── src/
	└── app/
		├── app.config.ts
		├── app.css
		├── app.html
		├── app.routes.ts
		├── app.spec.ts
		├── app.ts
		├── components/
		│   ├── dashboard/
		│   │   ├── dashboard.css
		│   │   ├── dashboard.html
		│   │   ├── dashboard.spec.ts
		│   │   └── dashboard.ts
		│   ├── header/
		│   │   ├── header.css
		│   │   ├── header.html
		│   │   ├── header.spec.ts
		│   │   └── header.ts
		│   ├── login/
		│   │   ├── login.css
		│   │   ├── login.html
		│   │   ├── login.spec.ts
		│   │   └── login.ts
		│   ├── product/
		│   │   ├── product.css
		│   │   ├── product.html
		│   │   ├── product.spec.ts
		│   │   └── product.ts
		│   ├── product-details/
		│   │   ├── product-details.css
		│   │   ├── product-details.html
		│   │   ├── product-details.spec.ts
		│   │   └── product-details.ts
		│   ├── products/
		│   │   ├── products.css
		│   │   ├── products.html
		│   │   ├── products.spec.ts
		│   │   └── products.ts
		│   └── profile/
		│       ├── profile.css
		│       ├── profile.html
		│       ├── profile.spec.ts
		│       └── profile.ts
		├── guards/
		│   └── auth.guard.ts
		├── models/
		│   ├── login.model.ts
		│   ├── product.model.ts
		│   └── user.model.ts
		├── rxjs/
		│   └── auth.operator.ts
		└── services/
		    ├── product.api.service.ts
		    └── user.api.service.ts
```

## File Functionality

- `src/app/app.config.ts`: Application-wide providers and bootstrap configuration.
- `src/app/app.css`: Root app component styles.
- `src/app/app.html`: Root app component template.
- `src/app/app.routes.ts`: Route definitions for navigation and guards.
- `src/app/app.spec.ts`: Root app test coverage.
- `src/app/app.ts`: Root app component that wires login and shell layout.
- `src/app/components/dashboard/dashboard.css`: Dashboard component styles.
- `src/app/components/dashboard/dashboard.html`: Dashboard component template.
- `src/app/components/dashboard/dashboard.spec.ts`: Dashboard component test coverage.
- `src/app/components/dashboard/dashboard.ts`: Dashboard component logic and user subscription handling.
- `src/app/components/header/header.css`: Header component styles.
- `src/app/components/header/header.html`: Header component template.
- `src/app/components/header/header.spec.ts`: Header component test coverage.
- `src/app/components/header/header.ts`: Header component logic for user display and logout.
- `src/app/components/login/login.css`: Login component styles.
- `src/app/components/login/login.html`: Login component template.
- `src/app/components/login/login.spec.ts`: Login component test coverage.
- `src/app/components/login/login.ts`: Login form logic, validation, and authentication flow.
- `src/app/components/product/product.css`: Product card styles.
- `src/app/components/product/product.html`: Product card template.
- `src/app/components/product/product.spec.ts`: Product component test coverage.
- `src/app/components/product/product.ts`: Reusable product display component.
- `src/app/components/product-details/product-details.css`: Product details styles.
- `src/app/components/product-details/product-details.html`: Product details template.
- `src/app/components/product-details/product-details.spec.ts`: Product details test coverage.
- `src/app/components/product-details/product-details.ts`: Product details view logic and API loading.
- `src/app/components/products/products.css`: Products list styles.
- `src/app/components/products/products.html`: Products list template.
- `src/app/components/products/products.spec.ts`: Products component test coverage.
- `src/app/components/products/products.ts`: Products listing logic and navigation.
- `src/app/components/profile/profile.css`: Profile component styles.
- `src/app/components/profile/profile.html`: Profile component template.
- `src/app/components/profile/profile.spec.ts`: Profile component test coverage.
- `src/app/components/profile/profile.ts`: Profile view logic and current user subscription.
- `src/app/guards/auth.guard.ts`: Route guard that protects authenticated routes.
- `src/app/models/login.model.ts`: Data model for login form state.
- `src/app/models/product.model.ts`: Data model for product information.
- `src/app/models/user.model.ts`: Data model for user information.
- `src/app/rxjs/auth.operator.ts`: Shared authentication stream and auth actions.
- `src/app/services/product.api.service.ts`: API client for product requests.
- `src/app/services/user.api.service.ts`: API client for user and login requests.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.8.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
