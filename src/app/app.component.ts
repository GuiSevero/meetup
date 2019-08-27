import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { map, switchMap, filter, debounceTime, distinct, tap, startWith } from 'rxjs/operators';
import { DocumentResult } from './app.models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Poatek - AWS Meetup - 2019';
  public searchTerm: string;

  public documents$: Observable<any>;
  public latestSearch = new Subject<string>();

  constructor(public http: HttpClient) {
    this.documents$ = this.latestSearch
    .pipe(
        startWith('')
      , debounceTime(200)
      , switchMap(term => this.searchDocuments(term))
    );
  }

  public search(term: string) {
    this.latestSearch.next(term);
  }

  private searchDocuments(query: string): Observable<any> {
    return this.http.get<DocumentResult>('https://x2x3k5pskb.execute-api.us-east-1.amazonaws.com/dev/documents', {
      params: {
        query
      }
    }).pipe(map(x => x.res));
  }
}
