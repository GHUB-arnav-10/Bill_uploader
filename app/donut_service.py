import torch
import re
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import fitz  
import io

class DonutService:
   
    def __init__(self, pretrained_model_name_or_path: str):
       
        print(f"Loading Donut model: {pretrained_model_name_or_path}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        try:
            self.processor = DonutProcessor.from_pretrained(pretrained_model_name_or_path)
            self.model = VisionEncoderDecoderModel.from_pretrained(pretrained_model_name_or_path)
            
            self.model.to(self.device)
            if self.device == "cuda":
                self.model.half()
            
            print("Donut model loaded successfully.")
        except Exception as e:
            print(f"Error loading Donut model: {e}")
            print("Please ensure you have a working internet connection and the model name is correct.")
            self.model = None
            self.processor = None

    def analyze(self, image: Image.Image, task_prompt: str) -> dict:
        
        if not self.model or not self.processor:
            return {"status": "error", "message": "Donut model is not loaded."}

        
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        decoder_input_ids = self.processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt"
        ).input_ids

        
        outputs = self.model.generate(
            pixel_values.to(self.device),
            decoder_input_ids=decoder_input_ids.to(self.device),
            max_length=self.model.decoder.config.max_position_embeddings,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        
        sequence = self.processor.batch_decode(outputs.sequences)[0]
        
        
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
        sequence = re.sub(f"^{re.escape(task_prompt)}", "", sequence).strip()
        
      
        try:
            result = self.processor.token2json(sequence)
            return {"status": "success", "data": result}
        except Exception as e:
            print(f"Failed to parse model output into JSON: {e}")
            print(f"Raw model output: {sequence}")
            return {"status": "error", "message": "Failed to parse model output.", "raw_output": sequence}

def convert_file_to_image(file_bytes: bytes, file_name: str) -> Image.Image:
   
    file_ext = file_name.split('.')[-1].lower()
    
    if file_ext == 'pdf':
        
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page = doc.load_page(0) 
        pix = page.get_pixmap(dpi=200) 
        doc.close()
        img_bytes = pix.tobytes("ppm")
        image = Image.open(io.BytesIO(img_bytes))
    else:
        
        image = Image.open(io.BytesIO(file_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
            
    return image
