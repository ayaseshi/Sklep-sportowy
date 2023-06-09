import { Component, OnInit, Input, AfterViewInit } from '@angular/core';
import { NavigationEnd, Router, ActivatedRoute } from '@angular/router';
import { filter } from 'rxjs/operators';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})

export class NavBarComponent implements OnInit, AfterViewInit {
  currentComponent: string | null = null;
  routeParams: any;
  @Input() itemId: string = ''; 
  @Input() itemName: string = ''; 
  @Input() itemCategory: string = ''; 
  @Input() itemBrand: string = ''; 
  @Input() notFound: string = ''; 

  constructor(private router: Router, private titleService: Title, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.currentComponent = this.getCurrentComponentName();
      });
  }

  ngAfterViewInit(): void {
    const currentUrl = this.router.url;
    let pageTitle = '';

    this.route.queryParams.subscribe(params => {
      if (params['brand']) {
        this.itemBrand = params['brand'];
      }
      if (params['category']) {
        this.itemCategory = params['category'];
      }

      if(this.itemName) {
        pageTitle = this.itemName + ' - AWAZONsport';
      } else if(this.itemBrand && this.itemBrand !== 'Wszystkie') {
        pageTitle = this.itemBrand + ' - AWAZONsport';  
      } else if(this.itemCategory && this.itemCategory !== 'Wszystkie') {
        pageTitle = this.itemCategory + ' - AWAZONsport';  
      } else if (currentUrl === '/login' && !currentUrl.includes('/login-google')) {
        pageTitle = 'Logowanie - AWAZONsport';
      } else if (currentUrl === '/register') {
        pageTitle = 'Rejestracja - AWAZONsport';
      } else if (currentUrl === '/cookies') {
        pageTitle = 'Polityka prywatności - AWAZONsport';
      } else if (currentUrl === '/rules') {
        pageTitle = 'Regulamin sprzedaży - AWAZONsport';
      } else if (currentUrl === '/cart') {
        pageTitle = 'Koszyk - AWAZONsport';
      } else if (currentUrl === '/checkout') {
        pageTitle = 'Kasa - AWAZONsport';
      } else if (currentUrl === '/payment-cancel') {
        pageTitle = 'Płatność anulowana - AWAZONsport';
      } else if (currentUrl === '/payment-success') {
        pageTitle = 'Płatność zakończona - AWAZONsport';
      } else if (currentUrl === '/orders') {
        pageTitle = 'Twoje zamówienia - AWAZONsport';
      } else if (currentUrl === '/admin-panel') {
        pageTitle = 'Panel administratora - AWAZONsport';
      } else if (currentUrl === '/admin-panel/orders') {
        pageTitle = 'Zamówienia - Panel administratora - AWAZONsport';
      } else if (currentUrl === '/admin-panel/product-list') {
        pageTitle = 'Lista produktów -Panel administratora - AWAZONsport';
      } else if (currentUrl === '/admin-panel/add-product') {
        pageTitle = 'Dodaj produkt - Panel administratora - AWAZONsport';
      } else if (currentUrl === ('/admin-panel/increase-stock/'+this.itemId)) {
        pageTitle = 'Dodaj do magazynu - Panel administratora - AWAZONsport';
      } else if (currentUrl === ('/admin-panel/edit-product/'+this.itemId)) {
        pageTitle = 'Edycja produktu - Panel administratora - AWAZONsport';
      } else if(this.notFound) {
        pageTitle = 'Nie znaleziono podanej strony - AWAZONsport';
      } else {
        pageTitle = 'Strona główna - AWAZONsport';
      }

      this.setPageTitle(pageTitle);
    });
  }

  private getCurrentComponentName(): string | null {
    const currentUrl = this.router.url;
    return currentUrl;
  }

  isCurrentComponent(componentName: string): boolean {
    return this.router.url.startsWith(componentName);
  }

  navigateToCategory(category: string): void {
    this.router.navigate([''], { queryParams: { category: category, brand: 'Wszystkie' } });
  }
  
  navigateToBrand(brand: string): void {
    this.router.navigate([''], { queryParams: { brand: brand, category: 'Wszystkie' } });
  }

  navigateToHomePage(): void {
    this.router.navigate([''], { queryParams: { brand: 'Wszystkie', category: 'Wszystkie' } });
  }

  setPageTitle(title: string): void {
    this.titleService.setTitle(title);
  }
}