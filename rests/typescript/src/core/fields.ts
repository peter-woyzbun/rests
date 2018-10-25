import {Model} from './model'


// -------------------------
// Foreign Key Field
//
// -------------------------

export const foreignKeyField = (RelatedModel: () => typeof Model) =>

  function(target: Model, propertyKey: string) {

    const _RelatedModel = RelatedModel();

    // Key for retrieving the ID value of this foreign key relation.
    const idPropertyKey = propertyKey + '_id';

    let value = target[propertyKey];
    let idValue = target[idPropertyKey];

    const getter = async () => {
        if (value){ return value }
        if (idValue){
            value = await _RelatedModel.objects.get(idValue);
            return value
        }
        return undefined
    };

    const setter = (val) => {
        if (val instanceof RelatedModel){
            value = val
        } else if (typeof val === 'number'){
            idValue = val
        } else {
            value = undefined;
            idValue = undefined;
        }
    };


    Object.defineProperty(target, propertyKey, {
        get: getter,
        set: setter
    });

  };
