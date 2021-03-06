import { Injectable } from "@angular/core";
import { Http, Response, Headers, RequestOptions } from "@angular/http";

import { Event } from "./event.model";
import { Observable } from "rxjs/Observable";
import "rxjs/add/observable/throw";

@Injectable()
export class EventService {
    private eventBaseUrl = "api/events/";
    private eventCreateUrl = "api/events/new/";
    private lastEvent: Event = null;

    constructor(private http: Http) {}

    public getEvent(id: number): Observable<Event> {
        if (this.lastEvent != null && this.lastEvent.id === id) {
            return Observable.of(this.lastEvent);
        }
        let headers = new Headers({ "Accept": "application/json" });
        let options = new RequestOptions({ headers: headers });
        return this.http.get(this.eventUrl(id), options)
            .map(this.extractEventData)
            .do(event => this.lastEvent = event)
            .catch(this.handleError);
    }

    public getTweetIds(event: Event, sinceId: string = ""): Observable<string[]> {
        return this.http.get(this.tweetsUrl(event.id, sinceId))
            .map(this.extractTweetData)
            .catch(error => Observable.of([]));
    }

    public addEvent (event: Event) {
        let headers = new Headers({ "Content-Type": "application/json" });
        let options = new RequestOptions({ headers: headers });
        return this.http.post(this.eventCreateUrl, event, options)
                        .map( res => { return "Vielen Dank für Ihren Beitrag.\n " +
                                              "Nach einer Prüfung werden wir das Event hinzufügen!"})
                        .catch(this.handleError);

    }

    private eventUrl(eventId: number): string {
        return `${this.eventBaseUrl}${eventId}`;
    }

    private tweetsUrl(eventId: number, sinceId: string): string {
        return `${this.eventUrl(eventId)}/tweets.json?since_id=${sinceId}`;
    }

    private extractEventData(response: Response): Event {
        let data = response.json();
        return <Event> data;
    }

    private extractTweetData(response: Response): string[] {
        let data = response.json() || [];
        return <string[]> data;
    }

    private handleError(error: any) {
        let errorMessage = "Interner Serverfehler";
        let parsedError = {'message':''};
        try {
            parsedError = (error._body) ? JSON.parse(error._body) : parsedError;
        } catch (e) { }
        if (parsedError.message) {
            errorMessage = parsedError.message;
        } else if (error.status) {
            errorMessage = `${error.status} - ${error.statusText}`;
        }
        console.error(errorMessage);
        return Observable.throw(errorMessage);
    }
}
