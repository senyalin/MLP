# Mathematical Language Processing
 * This is the code for the following paper: \
 Lin, Jason, Xing Wang, Zelun Wang, Donald Beyette, and Jyh-Charn Liu. "Prediction of mathematical expression declarations based on spatial, semantic, and syntactic analysis." In Proceedings of the ACM Symposium on Document Engineering 2019, pp. 1-10. 2019.
 * The main function is in 'dec_extractor.py', which will extract the semantics of mathematical expressions given a text.
 * Fit the sentence as a string with ME in "MATH_ID" format to the function extract_def_by_pattern, and it will return a dict with ME as key, and its declaration as value.
