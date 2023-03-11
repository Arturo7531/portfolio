import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

try:
    from datasets import Dataset
    from transformers import AutoTokenizer,Trainer, AutoModelForQuestionAnswering, logging #, pipeline
    #logger.error('ERROR')
    import pandas
    from tqdm.auto import tqdm
    #import evaluate
    import collections
    import numpy as np
    #import re
    #import tensorflow as tf
    #tf.logging.set_verbosity(tf.logging.ERROR)
    
except ImportError:
    print('Error: Please install the required packages. Exiting...')
    print('Required packages: datasets, transformers, pandas, tqdm, collections, numpy')


def main():
    print("\nWelcome to the Lawbot QA tool for contracts!")

    path = input('\nPlease input the path to your contract file. -> ')
    try:
        with open(path, 'r') as f:
            context = f.read() #.replace("\\n","").replace("\'", "'") #f.read() #.replace("\n", "")
            #context = re.sub(r'\\.',lambda x:{'\\n':'\n','\\t':'\t', '\n':'\n'}.get(x[0],x[0]),context)
            #print(context)
        print('\nFile found. Initiating QA process...')
    except FileNotFoundError:
        return print('\nError: File not found. Exiting...')
    question = input('\nPlease input your question. -> ')
    print('\nProcessing... This might take a couple minutes depending on question and context\n')
    #nlp = pipeline(model='arturo7531/nlp_roberta_legal', tokenizer=AutoTokenizer.from_pretrained('arturo7531/nlp_roberta_legal'), framework='pt')
    #answerset=nlp(question=question, context=context)

    #print(context)
    #print(context2)

    def transformer(context, question):
        new_review = {"context" : [context] , "question": [question], "id": [1]}
        df = pandas.DataFrame(data = new_review)
        small_eval_set = Dataset.from_pandas(df)
        return small_eval_set
    
    def preprocess_val_function(examples):
        tokenizer = AutoTokenizer.from_pretrained("saibo/legal-roberta-base")
        questions = [q.strip() for q in examples["question"]]
        inputs = tokenizer(
            questions,
            examples["context"],
            max_length=256,
            truncation="only_second",
            stride=64,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
        )

        sample_map = inputs.pop("overflow_to_sample_mapping") #extract the overflow_to_sample_mapping inputs key
        example_ids = []

        for i in range(len(inputs["input_ids"])): #For each feature
            sample_idx = sample_map[i] #position of the sample to which the feature belongs to -> 0
            example_ids.append(examples["id"][sample_idx]) #map the features to the sample id they correspond [list]

            sequence_ids = inputs.sequence_ids(i) # maps each token of the feature to whether it is a special character (None), the question (0) or the context (1) -> [None, 0,0,0, None, None, 1,1,1,1,1, None]
            offset = inputs["offset_mapping"][i] #list of token tuples with its start and end position
            inputs["offset_mapping"][i] = [
                o if sequence_ids[k] == 1 else None for k, o in enumerate(offset) #set the offsets corresponding to the question and special character to None, set to o for the ones corresponding to the answer
            ]

        inputs["example_id"] = example_ids #add a key to the input with the mapping of the features to the corresponding sample id
        return inputs

    def compute_metrics(start_logits, end_logits, features, examples):
        n_best = 20
        max_answer_length = 50 
        example_to_features = collections.defaultdict(list)
        for idx, feature in enumerate(features):
            example_to_features[feature["example_id"]].append(idx)

        predicted_answers = []
        for example in tqdm(examples):
            example_id = example["id"]
            context = example["context"]
            answers = []

            # Loop through all features associated with that example
            for feature_index in example_to_features[example_id]:
                start_logit = start_logits[feature_index]
                end_logit = end_logits[feature_index]
                offsets = features[feature_index]["offset_mapping"]

                start_indexes = np.argsort(start_logit)[-1 : -n_best - 1 : -1].tolist()
                end_indexes = np.argsort(end_logit)[-1 : -n_best - 1 : -1].tolist()
                for start_index in start_indexes:
                    for end_index in end_indexes:
                        # Skip answers that are not fully in the context
                        if offsets[start_index] is None or offsets[end_index] is None:
                            continue
                        # Skip answers with a length that is either < 0 or > max_answer_length
                        if (
                            end_index < start_index
                            or end_index - start_index + 1 > max_answer_length
                        ):
                            continue

                        answer = {
                            "text": context[offsets[start_index][0] : offsets[end_index][1]],
                            "logit_score": start_logit[start_index] + end_logit[end_index],
                        }
                        answers.append(answer)

            # Select the answer with the best score
            if len(answers) > 0:
                best_answer = max(answers, key=lambda x: x["logit_score"])
                predicted_answers.append(best_answer["text"])

        return predicted_answers #best_answer['text'] #predicted_answers

    logging.set_verbosity_error()
    #logger = logging.get_logger("transformers")

    small_eval_set = transformer(context, question)

    eval_set = small_eval_set.map(
        preprocess_val_function,
        batched=True,
        #batch_size=4,
        remove_columns=small_eval_set.column_names,
    )

    Final_Model = AutoModelForQuestionAnswering.from_pretrained("arturo7531/nlp_roberta_legal")
    model = Trainer(model=Final_Model)
    predictions, _, _ = model.predict(eval_set)
    start_logits, end_logits = predictions

    answer = compute_metrics(start_logits, end_logits, eval_set, small_eval_set)
    print('\nAnswer: ' + answer[0])



    #print('Answer: ', answerset['answer'])
    #print('Confidence: ', str(answerset['score']*100)[0:1]+'%')
    print('\nDone!')
    #print(logging.get_verbosity())
    
if __name__ == '__main__':
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
    os.environ["TRANSFORMERS_VERBOSITY"] = "error"
    os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
    main()