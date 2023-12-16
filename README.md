# AudioBookSync

<img src="https://s5.gifyu.com/images/Sitk1.gif" alt="Alt Text" width="400"/>

Welcome to AudioBookSync! 

With AudioBookSync, you can sync up the book that you are reading with the Audiobook. If you have ever switched between reading a book and listening to the audiobook for that book, **you might have found yourself trying to pinpoint the page that you are on in the book by jumping around the audiobook, listening to chunks of text and trying to triangulate where you are in the book. <ins>These days are over.</ins>** 

AudioBookSync allows you to switch between book and audiobook format easily by allowing you to search for just a few keywords that indicate where you are in the physical book and then receive the exact timestamp of where you are in the audiobook!

# Usage
To use AudioBookSync, simply clone the repository and run `python AudioBookSync` with the following arguments:

1. `--audio`:
   - Type: String
   - Description: Path to the audio file. Supported formats include mp3, mp4, mpeg, mpga, m4a, wav, and webm. If not specified, the model will use the transcription_path to search the transcription file for the search string.

2. `--transcription_path`:
   - Type: String (Default: None)
   - Description: Manually pass the path to the transcription file generated after transcription with Whisper. When supplied, the model will not run inference and will use the specified transcription file instead.

3. `--language`:
   - Type: String (Default: "en")
   - Description: Language code of the audio file. Default is set to 'en' for English.

4. `--batch_size`:
   - Type: Integer (Default: 16)
   - Description: Batch size for inference. Default is set to 16.

5. `--custom_transcription_path`:
   - Type: String (Default: None)
   - Description: Designate a custom path for the output file of the transcription. Default is the path to the audio file + SyncKey.json.

6. `--model_type`:
   - Type: String (Default: "tiny")
   - Description: Model type to use for inference. Possible values are 'tiny', 'base', 'small', 'medium', 'large', and 'large-v2'. Default is set to 'tiny'.

7. `--transcription_only`:
   - Type: Boolean flag (Default: False)
   - Description: Flag to indicate that only transcription is required. No ability to search the transcription will be provided when this flag is set to True.

8. `--device`:
   - Type: String (Default: "cuda")
   - Description: Device to use for inference. Possible values are 'cuda' and 'cpu'. Default is set to 'cuda'.
