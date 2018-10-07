import {ServerClient, ResponseHandlers} from "./server_client";
import {Model} from "./model";



export abstract class Queryset{

    static Model: typeof Model;
    static serverClient: ServerClient;

    protected lookups: object;
    protected excludedLookups: object;
    protected _or: Queryset[];

    constructor(lookups: object = {}, excludedLookups: object = {}){
        this.lookups = lookups;
        this.excludedLookups = excludedLookups;
        this._or = [];
    }

    public serverClient(): ServerClient{
        return this.constructor['serverClient'];
    }

    public Model(): typeof Model{
        return this.constructor['Model']
    }

    public static async get(primaryKey: string | number, responseHandlers: ResponseHandlers={} ): Promise<Model | undefined>{
        let responseData = await this.serverClient.get(`${this.Model.BASE_URL}/${primaryKey}/get/`, responseHandlers);

        if (responseData){return new this.constructor['Model'](responseData)}
        return undefined
    }

    public static async create(data: object, responseHandlers: ResponseHandlers={}): Promise<Model | undefined>{
        let responseData = await this.serverClient.post(`${this.Model.BASE_URL}/create/`, data, responseHandlers);
        if (responseData){return new this.Model(responseData)}
        return undefined
    }

    public filter(lookups: object): Queryset{
        let updatedLookups = this.lookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined){ updatedLookups[lookupKey] = lookupValue }
        });
        this.lookups = updatedLookups;
        return this;
    }

    public exclude(lookups: object): Queryset{
        let updatedLookups = this.excludedLookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined){ updatedLookups[lookupKey] = lookupValue }
        });
        this.excludedLookups = updatedLookups;
        return this;
    }

    public or(queryset: Queryset): Queryset{
        this._or.push(queryset);
        return this
    }

    public serialize(): object{
        return {
            filters: this.lookups,
            exclude: this.excludedLookups,
            or_: this._or.map((queryset) => queryset.serialize())
        }
    }

    public async values(responseHandlers: ResponseHandlers={}, ...fields: string[]): Promise<object[]>{
        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields);
        let responseData = await this.serverClient().get(`${this.Model().BASE_URL}/`, responseHandlers, urlQuery);
        return responseData;
    }

    public async pageValues(responseHandlers: ResponseHandlers={}, pageNum: number = 1, pageSize: number = 25, ...fields: string[]): Promise<{num_results: number, num_pages: number, data: object[]}>{
        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields) + "&page=" + pageNum + "&pagesize=" + pageSize;
        let responseData = await this.serverClient().get(`${this.Model().BASE_URL}/`, responseHandlers, urlQuery);
        return responseData;
    }

    public async retrieve(responseHandlers: ResponseHandlers={}): Promise<Model[] | undefined>{
        const urlQuery = "query=" + JSON.stringify(this.serialize());
        let responseData = await this.serverClient().get(`${this.Model().BASE_URL}/`, responseHandlers, urlQuery);
        return responseData.map((data) => new this.constructor["Model"](data) )
    }

}