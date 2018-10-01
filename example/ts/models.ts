import {ServerClient, ResponseHandlers} from './server_client'


// -------------------------
// Server Client
//
// -------------------------

const serverClient = new ServerClient('http://localhost:5000/');

// -------------------------
// Question QuerySet
//
// -------------------------

export interface QuestionLookups {
    choices__id?: number;
    choices__id__exact?: number;
    choices__id__iexact?: number;
    choices__id__gt?: number;
    choices__id__gte?: number;
    choices__id__lt?: number;
    choices__id__lte?: number;
    choices__id__in?: number[];
    choices__id__contains?: number;
    choices__id__icontains?: number;
    choices__id__startswith?: number;
    choices__id__istartswith?: number;
    choices__id__endswith?: number;
    choices__id__iendswith?: number;
    choices__id__range?: [number, number];
    choices__id__isnull?: number;
    choices__id__regex?: number;
    choices__id__iregex?: number;
    choices__question?: Question;
    choices__question__in?: Question[];
    choices__question__exact?: Question;
    choices__question__lt?: Question;
    choices__question__gt?: Question;
    choices__question__gte?: Question;
    choices__question__lte?: Question;
    choices__question__isnull?: Question;
    choices__choice_text?: string;
    choices__choice_text__exact?: string;
    choices__choice_text__iexact?: string;
    choices__choice_text__gt?: string;
    choices__choice_text__gte?: string;
    choices__choice_text__lt?: string;
    choices__choice_text__lte?: string;
    choices__choice_text__in?: string[];
    choices__choice_text__contains?: string;
    choices__choice_text__icontains?: string;
    choices__choice_text__startswith?: string;
    choices__choice_text__istartswith?: string;
    choices__choice_text__endswith?: string;
    choices__choice_text__iendswith?: string;
    choices__choice_text__range?: [string, string];
    choices__choice_text__isnull?: string;
    choices__choice_text__regex?: string;
    choices__choice_text__iregex?: string;
    choices__votes?: number;
    choices__votes__exact?: number;
    choices__votes__iexact?: number;
    choices__votes__gt?: number;
    choices__votes__gte?: number;
    choices__votes__lt?: number;
    choices__votes__lte?: number;
    choices__votes__in?: number[];
    choices__votes__contains?: number;
    choices__votes__icontains?: number;
    choices__votes__startswith?: number;
    choices__votes__istartswith?: number;
    choices__votes__endswith?: number;
    choices__votes__iendswith?: number;
    choices__votes__range?: [number, number];
    choices__votes__isnull?: number;
    choices__votes__regex?: number;
    choices__votes__iregex?: number;
    choices__votes__contained_by?: number;
    id?: number;
    id__exact?: number;
    id__iexact?: number;
    id__gt?: number;
    id__gte?: number;
    id__lt?: number;
    id__lte?: number;
    id__in?: number[];
    id__contains?: number;
    id__icontains?: number;
    id__startswith?: number;
    id__istartswith?: number;
    id__endswith?: number;
    id__iendswith?: number;
    id__range?: [number, number];
    id__isnull?: number;
    id__regex?: number;
    id__iregex?: number;
    question_text?: string;
    question_text__exact?: string;
    question_text__iexact?: string;
    question_text__gt?: string;
    question_text__gte?: string;
    question_text__lt?: string;
    question_text__lte?: string;
    question_text__in?: string[];
    question_text__contains?: string;
    question_text__icontains?: string;
    question_text__startswith?: string;
    question_text__istartswith?: string;
    question_text__endswith?: string;
    question_text__iendswith?: string;
    question_text__range?: [string, string];
    question_text__isnull?: string;
    question_text__regex?: string;
    question_text__iregex?: string;
    pub_date?: Date;
    pub_date__exact?: Date;
    pub_date__iexact?: Date;
    pub_date__gt?: Date;
    pub_date__gte?: Date;
    pub_date__lt?: Date;
    pub_date__lte?: Date;
    pub_date__in?: Date[];
    pub_date__contains?: Date;
    pub_date__icontains?: Date;
    pub_date__startswith?: Date;
    pub_date__istartswith?: Date;
    pub_date__endswith?: Date;
    pub_date__iendswith?: Date;
    pub_date__range?: [Date, Date];
    pub_date__isnull?: Date;
    pub_date__regex?: Date;
    pub_date__iregex?: Date;
    pub_date__year?: Date;
    pub_date__month?: Date;
    pub_date__day?: Date;
    pub_date__week_day?: Date;
    pub_date__week?: Date;
    pub_date__quarter?: Date;
    pub_date__contained_by?: Date;
    pub_date__hour?: Date;
    pub_date__minute?: Date;
    pub_date__second?: Date;
    pub_date__date?: Date;
    pub_date__time?: Date
}


export class QuestionQuerySet {

    protected lookups: QuestionLookups
    protected excludedLookups: QuestionLookups
    protected _or: QuestionQuerySet[]

    constructor(lookups: QuestionLookups = {}, excludedLookups: QuestionLookups = {}, _or: QuestionQuerySet[] = []) {
        this.lookups = lookups
        this.excludedLookups = excludedLookups
        this._or = _or
    }


    public static async create(data: QuestionData, responseHandlers: ResponseHandlers = {}) {

        let responseData = await serverClient.post(`/question/create/`, data, responseHandlers)
        if (responseData) {
            return new Question(responseData)
        }
        return undefined

    }

    public exclude(lookups: QuestionLookups): QuestionQuerySet {
        let updatedLookups = this.excludedLookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined) {
                updatedLookups[lookupKey] = lookupValue
            }
        })
        this.excludedLookups = updatedLookups;
        return this;
    }

    public static exclude(lookups: QuestionLookups): QuestionQuerySet {

        return new QuestionQuerySet({}, lookups)

    }

    public filter(lookups: QuestionLookups): QuestionQuerySet {
        let updatedLookups = this.lookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined) {
                updatedLookups[lookupKey] = lookupValue
            }
        })
        this.lookups = updatedLookups;
        return this;

    }

    public static filter(lookups: QuestionLookups): QuestionQuerySet {
        return new QuestionQuerySet(lookups, {})
    }

    public static async get(id: number, responseHandlers: ResponseHandlers = {}) {
        let responseData = await serverClient.get(`/question/${id}/get/`, responseHandlers)
        if (responseData) {
            return new Question(responseData)
        }
        return undefined
    }

    public or(queryset: QuestionQuerySet): QuestionQuerySet {

        this._or.push(queryset)
        return this

    }

    public async pageValues(pageNum: number = 1, pageSize: number = 25, responseHandlers: ResponseHandlers = {}, ...fields: QuestionFieldName[]): Promise<{ num_results: number, num_pages: number, data: object[] }> {
        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields) + "&page=" + pageNum + "&pagesize=" + pageSize;
        let responseData = await serverClient.get(`/question/`, responseHandlers, urlQuery)
        return responseData;

    }

    public async retrieve(responseHandlers: ResponseHandlers = {}): Promise<Question[] | undefined> {

        const urlQuery = "query=" + JSON.stringify(this.serialize())
        let responseData = await serverClient.get(`/question/`, responseHandlers, urlQuery)
        return responseData.map((data) => new Question(data))

    }

    public serialize(): object {

        return {
            filters: this.lookups,
            exclude: this.excludedLookups,
            or_: this._or.map((queryset) => queryset.serialize())
        }

    }

    public async values(responseHandlers: ResponseHandlers = {}, ...fields: QuestionFieldName[]): Promise<object[]> {

        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields)
        let responseData = await serverClient.get(`/question/`, responseHandlers, urlQuery)
        return responseData;

    }

}


// -------------------------
// Question
//
// -------------------------

interface QuestionData {
    id: number;
    question_text: string;
    pub_date: Date
}


type QuestionFieldName = "id" | "question_text" | "pub_date"


export class Question {

    id: number
    question_text: string
    pub_date: Date

    constructor({id, question_text, pub_date}: QuestionData) {
        this.id = id
        this.question_text = question_text
        this.pub_date = pub_date
    }


    public async delete(responseHandlers: ResponseHandlers = {}) {

        let response = await serverClient.delete(`/question/${ this.pk() }/delete/`, responseHandlers)

    }

    public pk(): number {

        return this.id

    }

    private _toData(): object {

        let data = {};
        Question.FIELDS.map((fieldName) => {
            if (fieldName !== 'id') {
                data[fieldName] = this[fieldName];
            }
        })
        return data;

    }

    public async save(responseHandlers: ResponseHandlers = {}) {

        let response = await serverClient.post(`/question/${ this.pk() }/update/`, this._toData(), responseHandlers)

    }

    public toData(): object {

        let data = {};
        Question.FIELDS.map((fieldName) => {
            data[fieldName] = this[fieldName];
        })
        return data;

    }

    public async update(data: Partial<QuestionData>, responseHandlers: ResponseHandlers = {}) {

        Object.keys(data).map((fieldName) => {
            this[fieldName] = data[fieldName];
        })
        await this.save();

    }


    public choices(): ChoiceQuerySet {

        return new ChoiceQuerySet({...{question__id: this.pk()}})

    }


    public static objects = QuestionQuerySet;
    public static readonly FIELDS = ["id", "question_text", "pub_date"];

}


// -------------------------
// Choice QuerySet
//
// -------------------------

export interface ChoiceLookups {
    id?: number;
    id__exact?: number;
    id__iexact?: number;
    id__gt?: number;
    id__gte?: number;
    id__lt?: number;
    id__lte?: number;
    id__in?: number[];
    id__contains?: number;
    id__icontains?: number;
    id__startswith?: number;
    id__istartswith?: number;
    id__endswith?: number;
    id__iendswith?: number;
    id__range?: [number, number];
    id__isnull?: number;
    id__regex?: number;
    id__iregex?: number;
    question__id?: number;
    question__id__exact?: number;
    question__id__iexact?: number;
    question__id__gt?: number;
    question__id__gte?: number;
    question__id__lt?: number;
    question__id__lte?: number;
    question__id__in?: number[];
    question__id__contains?: number;
    question__id__icontains?: number;
    question__id__startswith?: number;
    question__id__istartswith?: number;
    question__id__endswith?: number;
    question__id__iendswith?: number;
    question__id__range?: [number, number];
    question__id__isnull?: number;
    question__id__regex?: number;
    question__id__iregex?: number;
    question__question_text?: string;
    question__question_text__exact?: string;
    question__question_text__iexact?: string;
    question__question_text__gt?: string;
    question__question_text__gte?: string;
    question__question_text__lt?: string;
    question__question_text__lte?: string;
    question__question_text__in?: string[];
    question__question_text__contains?: string;
    question__question_text__icontains?: string;
    question__question_text__startswith?: string;
    question__question_text__istartswith?: string;
    question__question_text__endswith?: string;
    question__question_text__iendswith?: string;
    question__question_text__range?: [string, string];
    question__question_text__isnull?: string;
    question__question_text__regex?: string;
    question__question_text__iregex?: string;
    question__pub_date?: Date;
    question__pub_date__exact?: Date;
    question__pub_date__iexact?: Date;
    question__pub_date__gt?: Date;
    question__pub_date__gte?: Date;
    question__pub_date__lt?: Date;
    question__pub_date__lte?: Date;
    question__pub_date__in?: Date[];
    question__pub_date__contains?: Date;
    question__pub_date__icontains?: Date;
    question__pub_date__startswith?: Date;
    question__pub_date__istartswith?: Date;
    question__pub_date__endswith?: Date;
    question__pub_date__iendswith?: Date;
    question__pub_date__range?: [Date, Date];
    question__pub_date__isnull?: Date;
    question__pub_date__regex?: Date;
    question__pub_date__iregex?: Date;
    question__pub_date__year?: Date;
    question__pub_date__month?: Date;
    question__pub_date__day?: Date;
    question__pub_date__week_day?: Date;
    question__pub_date__week?: Date;
    question__pub_date__quarter?: Date;
    question__pub_date__contained_by?: Date;
    question__pub_date__hour?: Date;
    question__pub_date__minute?: Date;
    question__pub_date__second?: Date;
    question__pub_date__date?: Date;
    question__pub_date__time?: Date;
    question?: Question;
    question__in?: Question[];
    question__exact?: Question;
    question__lt?: Question;
    question__gt?: Question;
    question__gte?: Question;
    question__lte?: Question;
    question__isnull?: Question;
    choice_text?: string;
    choice_text__exact?: string;
    choice_text__iexact?: string;
    choice_text__gt?: string;
    choice_text__gte?: string;
    choice_text__lt?: string;
    choice_text__lte?: string;
    choice_text__in?: string[];
    choice_text__contains?: string;
    choice_text__icontains?: string;
    choice_text__startswith?: string;
    choice_text__istartswith?: string;
    choice_text__endswith?: string;
    choice_text__iendswith?: string;
    choice_text__range?: [string, string];
    choice_text__isnull?: string;
    choice_text__regex?: string;
    choice_text__iregex?: string;
    votes?: number;
    votes__exact?: number;
    votes__iexact?: number;
    votes__gt?: number;
    votes__gte?: number;
    votes__lt?: number;
    votes__lte?: number;
    votes__in?: number[];
    votes__contains?: number;
    votes__icontains?: number;
    votes__startswith?: number;
    votes__istartswith?: number;
    votes__endswith?: number;
    votes__iendswith?: number;
    votes__range?: [number, number];
    votes__isnull?: number;
    votes__regex?: number;
    votes__iregex?: number;
    votes__contained_by?: number
}


export class ChoiceQuerySet {

    protected lookups: ChoiceLookups
    protected excludedLookups: ChoiceLookups
    protected _or: ChoiceQuerySet[]

    constructor(lookups: ChoiceLookups = {}, excludedLookups: ChoiceLookups = {}, _or: ChoiceQuerySet[] = []) {
        this.lookups = lookups
        this.excludedLookups = excludedLookups
        this._or = _or
    }


    public static async create(data: ChoiceData, responseHandlers: ResponseHandlers = {}) {

        let responseData = await serverClient.post(`/choice/create/`, data, responseHandlers)
        if (responseData) {
            return new Choice(responseData)
        }
        return undefined

    }

    public exclude(lookups: ChoiceLookups): ChoiceQuerySet {

        let updatedLookups = this.excludedLookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined) {
                updatedLookups[lookupKey] = lookupValue
            }
        })
        this.excludedLookups = updatedLookups;
        return this;

    }

    public static exclude(lookups: ChoiceLookups): ChoiceQuerySet {

        return new ChoiceQuerySet({}, lookups)

    }

    public filter(lookups: ChoiceLookups): ChoiceQuerySet {

        let updatedLookups = this.lookups;
        Object.keys(lookups).map((lookupKey) => {
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined) {
                updatedLookups[lookupKey] = lookupValue
            }
        })
        this.lookups = updatedLookups;
        return this;

    }

    public static filter(lookups: ChoiceLookups): ChoiceQuerySet {

        return new ChoiceQuerySet(lookups, {})

    }

    public static async get(id: number, responseHandlers: ResponseHandlers = {}) {

        let responseData = await serverClient.get(`/choice/${id}/get/`, responseHandlers)
        if (responseData) {
            return new Choice(responseData)
        }
        return undefined

    }

    public or(queryset: ChoiceQuerySet): ChoiceQuerySet {

        this._or.push(queryset)
        return this

    }

    public async pageValues(pageNum: number = 1, pageSize: number = 25, responseHandlers: ResponseHandlers = {}, ...fields: ChoiceFieldName[]): Promise<{ num_results: number, num_pages: number, data: object[] }> {

        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields) + "&page=" + pageNum + "&pagesize=" + pageSize;
        let responseData = await serverClient.get(`/choice/`, responseHandlers, urlQuery)
        return responseData;

    }

    public async retrieve(responseHandlers: ResponseHandlers = {}): Promise<Choice[] | undefined> {

        const urlQuery = "query=" + JSON.stringify(this.serialize())
        let responseData = await serverClient.get(`/choice/`, responseHandlers, urlQuery)
        return responseData.map((data) => new Choice(data))

    }

    public serialize(): object {

        return {
            filters: this.lookups,
            exclude: this.excludedLookups,
            or_: this._or.map((queryset) => queryset.serialize())
        }

    }

    public async values(responseHandlers: ResponseHandlers = {}, ...fields: ChoiceFieldName[]): Promise<object[]> {

        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields)
        let responseData = await serverClient.get(`/choice/`, responseHandlers, urlQuery)
        return responseData;

    }


}


// -------------------------
// Choice
//
// -------------------------

interface ChoiceData {
    id: number;
    _question: Question;
    question_id: number;
    choice_text: string;
    votes: number
}


type ChoiceFieldName = "id" | "_question" | "question_id" | "choice_text" | "votes"


export class Choice {

    id: number
    _question: Question
    question_id: number
    choice_text: string
    votes: number

    constructor({id, _question, question_id, choice_text, votes}: ChoiceData) {
        this.id = id
        this._question = _question
        this.question_id = question_id
        this.choice_text = choice_text
        this.votes = votes
    }


    public async delete(responseHandlers: ResponseHandlers = {}) {

        let response = await serverClient.delete(`/choice/${ this.pk() }/delete/`, responseHandlers)

    }

    public pk(): number {

        return this.id

    }

    private _toData(): object {

        let data = {};
        Choice.FIELDS.map((fieldName) => {
            if (fieldName !== 'id') {
                data[fieldName] = this[fieldName];
            }
        })
        return data;

    }

    public async save(responseHandlers: ResponseHandlers = {}) {

        let response = await serverClient.post(`/choice/${ this.pk() }/update/`, this._toData(), responseHandlers)

    }

    public toData(): object {

        let data = {};
        Choice.FIELDS.map((fieldName) => {
            data[fieldName] = this[fieldName];
        })
        return data;

    }

    public async update(data: Partial<ChoiceData>, responseHandlers: ResponseHandlers = {}) {

        Object.keys(data).map((fieldName) => {
            this[fieldName] = data[fieldName];
        })
        await this.save();

    }


    public get question(): undefined | Promise<Question | undefined> | Question {

        if (!this.question_id) {
            return undefined
        }
        if (this._question) {
            return this._question
        }
        return (async () => {
            return await this._getQuestion();
        })();

    }

    private async _getQuestion(): Promise<Question | undefined> {

        if (this.question_id !== undefined) {
            const question = await Question.objects.get(this.question_id);
            this._question = question
            return question
        }
        return undefined

    }

    public set question(question: undefined | Promise<Question | undefined> | Question) {

        if (question instanceof Question) {
            this.question_id = question.pk();
            this._question = question;
        } else {
            this.question_id = undefined;
            this._question = undefined;
        }

    }


    public static objects = ChoiceQuerySet;
    public static readonly FIELDS = ["id", "_question", "question_id", "choice_text", "votes"];

}

    
    

    