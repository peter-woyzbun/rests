import {Model} from './model'


// -------------------------
// Field Types
//
// -------------------------

export enum FieldType{
    CharField = "CharField",
    IntegerField = "IntegerField",
    ForeignKey = "ForeignKey",
    OneToOneField = "OneToOneField",
    JSONField = "JSONField",
    ArrayField = "ArrayField",
    FloatField = "FloatField",
    TextField = "TextField",
    BooleanField = "BooleanField",
    DateField = "DateField",
    DateTimeField = "DateTimeField",
    AutoField = "AutoField",
    EncryptedField = "EncryptedField",
    EmailField = "EmailField",
    ManyToManyField = "ManyToManyField",
    PartitionField = "PartitionField"
}

// -------------------------
// Field Schema
//
// -------------------------


export interface FieldSchema{
    readonly fieldName: string;
    readonly fieldType: FieldType;
    readonly nullable: boolean;
    readonly isReadOnly: boolean;
    readonly description?: string;
    readonly defaultValue?: any;
    readonly relatedModel?: any;
    readonly choices?: any[]
}

// -------------------------
// Model Fields Schema
//
// -------------------------

export interface ModelFieldsSchema{
    [key: string]: FieldSchema
}