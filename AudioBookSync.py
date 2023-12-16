import whisperx
import json
import time
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Welcome to AudioBookSync! Sync up the book that you are reading with the Audiobook. If you are frequently switching between reading a book and listening to the audiobook for that book, you might have thought that it takes a ton of time to sync up where you are between the audio and physical text format. AudioBookSync allows you to search for just a few key words that indicate where you are in the physical book and receive the exact timestamp of where you are in the audiobook.")

parser.add_argument("--audio", type=str,
                    help="Path to the audio file. Supported formats are mp3, mp4, mpeg, mpga, m4a, wav, and webm. If audio is not specified, the model will use the transcription_path to search the transcription file for the search string.")

parser.add_argument("--transcription_path", type=str, default=None,
                    help="Manually pass the path to the transcription file that was generated after transcription with Whisper. When transcription_path is supplied, the model will not run inference and will use the transcription file instead.")

parser.add_argument("--language", type=str, default="en",
                    help="Language code of the audio file. Default is 'en' for English.")

parser.add_argument("--batch_size", type=int, default=16,
                    help="Batch size for inference. Default is 16")

parser.add_argument("--custom_transcription_path", type=str, default=None,
                    help="Designate a custom path for the output file of the transcription. Default is the path to the audio file + SyncKey.json")

parser.add_argument("--model_type", type=str, default="tiny",
                    help="Model type to use for inference. Possible values are 'tiny', 'base', 'small', 'medium', 'large', and 'large-v2'. Default is 'tiny")
# Add flag transcription only that doesnt do the search
parser.add_argument("--transcription_only", action="store_true",
                    help="Flag to indicate that only transcription is required. No ability to search the transcription will be provided. Default is False")

parser.add_argument("--device", type=str, default="cuda",
                    help="Device to use for inference. Possible values are 'cuda' and 'cpu'. Default is 'cuda.'")
args = parser.parse_args()

# Check if at least one of --audio or --transcription_path is provided
if not (args.audio or args.transcription_path):
    parser.print_help()
    sys.exit("Error: At least one of --audio or --transcription_path is required.")

if args.transcription_path == None:
    compute_type = "float16"
    model = whisperx.load_model(
        args.model_type, device=args.device, compute_type=compute_type, language=args.language)
    audio = whisperx.load_audio(args.audio)
    print(f"Audio for {args.audio} has been loaded successfully.")
    start = time.time()
    print("Transcribing Audio. This may take a while.")
    result = model.transcribe(audio, batch_size=args.batch_size)

    transcription_path = args.custom_transcription_path
    if transcription_path == None:
        transcription_path = args.audio.split(".")[0] + "SyncKey.json"

    with open(transcription_path, "w") as f:
        json.dump(result["segments"], f, indent=2)

    print(f"Transcription Complete and saved to {transcription_path}.")
    # Total time taken in minutes and seconds
    end = time.time()
    print(
        f"Total Transcription Processing Time: {int((end - start)//60)} Minutes, {int((end - start) % 60)} Seconds")


if not args.transcription_only:
    if args.transcription_path != None:
        syncKey = json.load(open(args.transcription_path, encoding='utf-8'))
    else:
        syncKey = result["segments"]

    while (1):
        searchString = input("Enter your search string: ")
        print()

        for segment in syncKey:
            # print(segment)
            if searchString.lower() in segment['text'].lower():
                # print the search string as well as 100 words before and after
                index = segment['text'].lower().index(searchString.lower())
                # print 100 words following the search string
                print("Relevant Text:",
                      segment['text'][index:index+200].strip())

                startHours = int(segment['start']//3600)
                startMinutes = int((segment['start'] % 3600)//60)
                startSeconds = int(segment['start'] % 60)
                endHours = int(segment['end']//3600)
                endMinutes = int((segment['end'] % 3600)//60)
                endSeconds = int(segment['end'] % 60)

                print(
                    f"Start time: {startHours} Hours, {startMinutes} Minutes, {startSeconds} Seconds")
                print(
                    f"End time: {endHours} Hours, {endMinutes} Minutes, {endSeconds} Seconds")
                print()
