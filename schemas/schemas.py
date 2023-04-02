from pydantic import BaseModel

class Email(BaseModel):
    task_id: str
    email_addr: str

    class Config:
        schema_extra = {
            "example": {
                "task_id": "5ae2e3f221c38a28845f05",
                "email_addr":
                    "alya.azhar@ui.ac.id"
            }
        }

class BookmarkEmail(BaseModel):
    email_addr: str

    class Config:
        schema_extra = {
            "example": {
                "email_addr":
                    "alya.azhar@ui.ac.id"
            }
        }


class PlacesToGo(BaseModel):
    index_id:str
    place_id:str
    name:str
    address:str
    url:str
    notes:str

    class Config:
        schema_extra = {
            "example": {
                "place_id" : "ChIJQVLTi_Idby4RNTCqjOVFHnU",
                "name" : "Distro Topeng Cirebon",
                "address": "Kios Pasar Seni No.8, Jalan Sunyaragi, Sunyaragi, Kec. Kesambi, Kota Cirebon, Jawa Barat 45132, Indonesia",
                "url": "https://maps.google.com/?cid=8439259603948679221",
                "notes":"Harus dikunjungi saat lebaran nanti!"
            }
        }    

class BookmarkRecommend(BaseModel):
    task_id:str
    class Config:
        schema_extra = {
            "example": {
                "task_id": "5ae2e3f221c38a28845f05"
            }
        }

"""
1. bisa nambah sendiri -> lebih ke bookmark
- mendingan ambil dari api detail gaksih?
- id bookmark
- id tempat lokasi ()
- nama lokasi
- alamat lokasi
- url gmaps -> butuh
2. bisa dari hasil rekomendasi
- id bookmark
- tiap hasil dari rekomendasi akan diiterasi dan di append,
baik pagi, siang, sore
"""


