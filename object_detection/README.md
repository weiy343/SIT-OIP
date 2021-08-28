###Yolov5 Folder/Files Breakdown Structure:

├── test folder                                           # Testing Dataset (70% - 84 images)
├── train folder                                          # Training Dataset (20% - 24 images)
├── val folder                                            # Validation Dataset (10% - 12 images)
├── content/yolov5 (Listing the ones I work on/use)
  ├── models
     ├── custom_yolov5s.yaml                              # Trained model
     ├── tf.py                                            # Convert to tensorflowlite
     ├── yolov5s.yaml                                     # Used to train model
  ├── runs
     ├── detect                                           # Images of test images + accuracy.
     ├── train                                            # After-training model documents/results (weights are in Google Drive bc file too big)
        ├── weights                                       ## https://drive.google.com/drive/folders/1fWynljLiQ9SoH2BsjfTevfCAYLwJMQ0V?usp=sharing
  ├── wandb                                               # After-training logs stored in wandb 
  ├── detect.py                                           # Used to test model
  ├── train.py                                            # Used to train model
├── Syringe_Detection.ipynb                               # Set up + training + detect (I run on Google Colab)
├── data.yaml                                             # Dataset file
