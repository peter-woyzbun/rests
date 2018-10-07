import { Model } from './core/model'
import { Queryset } from './core/queryset'
import { foreignKeyField } from './core/fields'
import { ResponseHandlers } from './core/server_client'
import { serverClient } from './client'

// -------------------------
// Question QuerySet
//
// -------------------------

interface QuestionLookups {
    choices__id?: number,
    choices__id__exact?: number,
    choices__id__iexact?: number,
    choices__id__gt?: number,
    choices__id__gte?: number,
    choices__id__lt?: number,
    choices__id__lte?: number,
    choices__id__in?: number[],
    choices__id__contains?: number,
    choices__id__icontains?: number,
    choices__id__startswith?: number,
    choices__id__istartswith?: number,
    choices__id__endswith?: number,
    choices__id__iendswith?: number,
    choices__id__range?: [number, number],
    choices__id__isnull?: number,
    choices__id__regex?: number,
    choices__id__iregex?: number,
    choices__question?: Question,
    choices__question__in?: Question[],
    choices__question__exact?: Question,
    choices__question__lt?: Question,
    choices__question__gt?: Question,
    choices__question__gte?: Question,
    choices__question__lte?: Question,
    choices__question__isnull?: Question,
    choices__choice_text?: string,
    choices__choice_text__exact?: string,
    choices__choice_text__iexact?: string,
    choices__choice_text__gt?: string,
    choices__choice_text__gte?: string,
    choices__choice_text__lt?: string,
    choices__choice_text__lte?: string,
    choices__choice_text__in?: string[],
    choices__choice_text__contains?: string,
    choices__choice_text__icontains?: string,
    choices__choice_text__startswith?: string,
    choices__choice_text__istartswith?: string,
    choices__choice_text__endswith?: string,
    choices__choice_text__iendswith?: string,
    choices__choice_text__range?: [string, string],
    choices__choice_text__isnull?: string,
    choices__choice_text__regex?: string,
    choices__choice_text__iregex?: string,
    choices__votes?: number,
    choices__votes__exact?: number,
    choices__votes__iexact?: number,
    choices__votes__gt?: number,
    choices__votes__gte?: number,
    choices__votes__lt?: number,
    choices__votes__lte?: number,
    choices__votes__in?: number[],
    choices__votes__contains?: number,
    choices__votes__icontains?: number,
    choices__votes__startswith?: number,
    choices__votes__istartswith?: number,
    choices__votes__endswith?: number,
    choices__votes__iendswith?: number,
    choices__votes__range?: [number, number],
    choices__votes__isnull?: number,
    choices__votes__regex?: number,
    choices__votes__iregex?: number,
    choices__votes__contained_by?: number,
    id?: number,
    id__exact?: number,
    id__iexact?: number,
    id__gt?: number,
    id__gte?: number,
    id__lt?: number,
    id__lte?: number,
    id__in?: number[],
    id__contains?: number,
    id__icontains?: number,
    id__startswith?: number,
    id__istartswith?: number,
    id__endswith?: number,
    id__iendswith?: number,
    id__range?: [number, number],
    id__isnull?: number,
    id__regex?: number,
    id__iregex?: number,
    question_text?: string,
    question_text__exact?: string,
    question_text__iexact?: string,
    question_text__gt?: string,
    question_text__gte?: string,
    question_text__lt?: string,
    question_text__lte?: string,
    question_text__in?: string[],
    question_text__contains?: string,
    question_text__icontains?: string,
    question_text__startswith?: string,
    question_text__istartswith?: string,
    question_text__endswith?: string,
    question_text__iendswith?: string,
    question_text__range?: [string, string],
    question_text__isnull?: string,
    question_text__regex?: string,
    question_text__iregex?: string,
    pub_date?: Date,
    pub_date__exact?: Date,
    pub_date__iexact?: Date,
    pub_date__gt?: Date,
    pub_date__gte?: Date,
    pub_date__lt?: Date,
    pub_date__lte?: Date,
    pub_date__in?: Date[],
    pub_date__contains?: Date,
    pub_date__icontains?: Date,
    pub_date__startswith?: Date,
    pub_date__istartswith?: Date,
    pub_date__endswith?: Date,
    pub_date__iendswith?: Date,
    pub_date__range?: [Date, Date],
    pub_date__isnull?: Date,
    pub_date__regex?: Date,
    pub_date__iregex?: Date,
    pub_date__year?: Date,
    pub_date__month?: Date,
    pub_date__day?: Date,
    pub_date__week_day?: Date,
    pub_date__week?: Date,
    pub_date__quarter?: Date,
    pub_date__contained_by?: Date,
    pub_date__hour?: Date,
    pub_date__minute?: Date,
    pub_date__second?: Date,
    pub_date__date?: Date,
    pub_date__time?: Date,

}

export class QuestionQueryset extends Queryset {

    static Model: typeof Question;
    static serverClient = serverClient;

    protected lookups: QuestionLookups;
    protected excludedLookups: QuestionLookups;
    protected _or: QuestionQueryset[];

    constructor(lookups: QuestionLookups = {}, excludedLookups: QuestionLookups = {}) {
        super(lookups, excludedLookups)
    }

    public static filter(lookups: QuestionLookups): QuestionQueryset {
        return new QuestionQueryset(lookups)
    }

    public static async get(primaryKey: string | number, responseHandlers: ResponseHandlers = {}): Promise<Question | undefined> {
        let responseData = await this.serverClient.get(`${this.Model.BASE_URL}/${primaryKey}/get/`, responseHandlers);

        if (responseData) { return new this.Model(responseData) }
        return undefined
    }

}



// -------------------------
// Question
//
// -------------------------

interface QuestionData {
    id: number,
    question_text: string,
    pub_date: Date,

}


export class Question extends Model {

    static BASE_URL = '/question';
    static PK_FIELD_NAME = 'id';
    static FIELDS = ['id', 'question_text', 'pub_date'];

    static objects = QuestionQueryset;
    static serverClient = serverClient;


    id: number;

    question_text: string;

    pub_date: Date;


    constructor({ id, question_text, pub_date }: QuestionData) {
        super({ id, question_text, pub_date })
    }

    public async update(data: Partial<QuestionData>, responseHandlers: ResponseHandlers = {}): Promise<Question> {
        Object.keys(data).map((fieldName) => {
            this[fieldName] = data[fieldName];
        });
        await this.save();
        return this;
    }


    public choices(lookups: ChoiceLookups = {}) {
        return new ChoiceQueryset({ ...lookups, ...{ question__id: this.pk() } })
    }


}

QuestionQueryset.Model = Question;



// -------------------------
// Choice QuerySet
//
// -------------------------

interface ChoiceLookups {
    id?: number,
    id__exact?: number,
    id__iexact?: number,
    id__gt?: number,
    id__gte?: number,
    id__lt?: number,
    id__lte?: number,
    id__in?: number[],
    id__contains?: number,
    id__icontains?: number,
    id__startswith?: number,
    id__istartswith?: number,
    id__endswith?: number,
    id__iendswith?: number,
    id__range?: [number, number],
    id__isnull?: number,
    id__regex?: number,
    id__iregex?: number,
    question__id?: number,
    question__id__exact?: number,
    question__id__iexact?: number,
    question__id__gt?: number,
    question__id__gte?: number,
    question__id__lt?: number,
    question__id__lte?: number,
    question__id__in?: number[],
    question__id__contains?: number,
    question__id__icontains?: number,
    question__id__startswith?: number,
    question__id__istartswith?: number,
    question__id__endswith?: number,
    question__id__iendswith?: number,
    question__id__range?: [number, number],
    question__id__isnull?: number,
    question__id__regex?: number,
    question__id__iregex?: number,
    question__question_text?: string,
    question__question_text__exact?: string,
    question__question_text__iexact?: string,
    question__question_text__gt?: string,
    question__question_text__gte?: string,
    question__question_text__lt?: string,
    question__question_text__lte?: string,
    question__question_text__in?: string[],
    question__question_text__contains?: string,
    question__question_text__icontains?: string,
    question__question_text__startswith?: string,
    question__question_text__istartswith?: string,
    question__question_text__endswith?: string,
    question__question_text__iendswith?: string,
    question__question_text__range?: [string, string],
    question__question_text__isnull?: string,
    question__question_text__regex?: string,
    question__question_text__iregex?: string,
    question__pub_date?: Date,
    question__pub_date__exact?: Date,
    question__pub_date__iexact?: Date,
    question__pub_date__gt?: Date,
    question__pub_date__gte?: Date,
    question__pub_date__lt?: Date,
    question__pub_date__lte?: Date,
    question__pub_date__in?: Date[],
    question__pub_date__contains?: Date,
    question__pub_date__icontains?: Date,
    question__pub_date__startswith?: Date,
    question__pub_date__istartswith?: Date,
    question__pub_date__endswith?: Date,
    question__pub_date__iendswith?: Date,
    question__pub_date__range?: [Date, Date],
    question__pub_date__isnull?: Date,
    question__pub_date__regex?: Date,
    question__pub_date__iregex?: Date,
    question__pub_date__year?: Date,
    question__pub_date__month?: Date,
    question__pub_date__day?: Date,
    question__pub_date__week_day?: Date,
    question__pub_date__week?: Date,
    question__pub_date__quarter?: Date,
    question__pub_date__contained_by?: Date,
    question__pub_date__hour?: Date,
    question__pub_date__minute?: Date,
    question__pub_date__second?: Date,
    question__pub_date__date?: Date,
    question__pub_date__time?: Date,
    question?: Question,
    question__in?: Question[],
    question__exact?: Question,
    question__lt?: Question,
    question__gt?: Question,
    question__gte?: Question,
    question__lte?: Question,
    question__isnull?: Question,
    choice_text?: string,
    choice_text__exact?: string,
    choice_text__iexact?: string,
    choice_text__gt?: string,
    choice_text__gte?: string,
    choice_text__lt?: string,
    choice_text__lte?: string,
    choice_text__in?: string[],
    choice_text__contains?: string,
    choice_text__icontains?: string,
    choice_text__startswith?: string,
    choice_text__istartswith?: string,
    choice_text__endswith?: string,
    choice_text__iendswith?: string,
    choice_text__range?: [string, string],
    choice_text__isnull?: string,
    choice_text__regex?: string,
    choice_text__iregex?: string,
    votes?: number,
    votes__exact?: number,
    votes__iexact?: number,
    votes__gt?: number,
    votes__gte?: number,
    votes__lt?: number,
    votes__lte?: number,
    votes__in?: number[],
    votes__contains?: number,
    votes__icontains?: number,
    votes__startswith?: number,
    votes__istartswith?: number,
    votes__endswith?: number,
    votes__iendswith?: number,
    votes__range?: [number, number],
    votes__isnull?: number,
    votes__regex?: number,
    votes__iregex?: number,
    votes__contained_by?: number,

}

export class ChoiceQueryset extends Queryset {

    static Model: typeof Choice;
    static serverClient = serverClient;

    protected lookups: ChoiceLookups;
    protected excludedLookups: ChoiceLookups;
    protected _or: ChoiceQueryset[];

    constructor(lookups: ChoiceLookups = {}, excludedLookups: ChoiceLookups = {}) {
        super(lookups, excludedLookups)
    }

    public static filter(lookups: ChoiceLookups): ChoiceQueryset {
        return new ChoiceQueryset(lookups)
    }

    public static async get(primaryKey: string | number, responseHandlers: ResponseHandlers = {}): Promise<Choice | undefined> {
        let responseData = await this.serverClient.get(`${this.Model.BASE_URL}/${primaryKey}/get/`, responseHandlers);

        if (responseData) { return new this.Model(responseData) }
        return undefined
    }

}



// -------------------------
// Choice
//
// -------------------------

interface ChoiceData {
    id: number,
    question: Question,
    question_id: Question,
    choice_text: string,
    votes: number,

}


export class Choice extends Model {

    static BASE_URL = '/choice';
    static PK_FIELD_NAME = 'id';
    static FIELDS = ['id', 'question', 'question_id', 'choice_text', 'votes'];

    static objects = ChoiceQueryset;
    static serverClient = serverClient;


    id: number;

    @foreignKeyField(Question) question: Question;

    question_id: Question;

    choice_text: string;

    votes: number;


    constructor({ id, question, question_id, choice_text, votes }: ChoiceData) {
        super({ id, question, question_id, choice_text, votes })
    }

    public async update(data: Partial<ChoiceData>, responseHandlers: ResponseHandlers = {}): Promise<Choice> {
        Object.keys(data).map((fieldName) => {
            this[fieldName] = data[fieldName];
        });
        await this.save();
        return this;
    }



}

ChoiceQueryset.Model = Choice;

