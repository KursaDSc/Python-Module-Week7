
class Validator:
    """
    Validator sınıfı, kullanıcı doğrulama ve veri formatı kontrolü için çeşitli yöntemler içerir.
    """
    
    def __init__(self):
        pass

        
    @staticmethod
    def validate_user(input_username, input_password, users_db):
        """
        Kullanıcı adı ve parola doğrulaması yapar.
        users_db: {'kullanici_adi': {'password': 'parola', 'role': 'admin/normal'}}
        Doğruysa rolünü döner, yanlışsa None döner.
        """
        try:
            input_username = input_username.strip()
            input_password = input_password.strip()

            for user in users_db:
                username, password, role = user
                if username == input_username and password == input_password:
                    return role
            return None
        except Exception as e:
            print(f"Kullanıcı doğrulama hatası: {e}")
            return None
    
    @staticmethod
    def validate_email(email):
        """
        E-posta adresinin geçerli bir formatta olup olmadığını kontrol eder.
        Basit bir regex ile doğrulama yapar.
        """
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_phone(phone):
        """
        Telefon numarasının geçerli bir formatta olup olmadığını kontrol eder.
        Basit bir regex ile doğrulama yapar.
        Türkiye için 10 haneli ve 5 ile başlayan numaraları kabul eder.
        """
        import re
        phone_regex = r'^(05[0-9]{9})$'
        return re.match(phone_regex, phone) is not None

    @staticmethod
    def validate_name(name):
        """
        İsim ve soyadının geçerli bir formatta olup olmadığını kontrol eder.
        Sadece harf ve boşluk karakterlerine izin verir.
        """
        import re
        name_regex = r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$'
        return re.match(name_regex, name) is not None

    @staticmethod
    def validate_date(date_str):
        """
        Tarih formatının geçerli olup olmadığını kontrol eder.
        YYYY-AA-GG formatında olmalıdır.
        """
        from datetime import datetime
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
      
    @staticmethod    
    def validate_time(time_str):
        """
        Saat formatının geçerli olup olmadığını kontrol eder.
        HH:MM formatında olmalıdır.
        """
        from datetime import datetime
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod    
    def validate_number(number_str):
        """
        Sayı formatının geçerli olup olmadığını kontrol eder.
        Sadece rakam ve ondalık noktasına izin verir.
        """
        import re
        number_regex = r'^\d+(\.\d+)?$'
        return re.match(number_regex, number_str) is not None

