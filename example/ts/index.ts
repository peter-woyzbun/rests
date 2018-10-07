import {Question} from "./server/models";


const results = Question.objects.filter({question_text__contains})