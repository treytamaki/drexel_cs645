package mitm;

import java.security.*;
import java.io.*;
import java.security.spec.*;
import javax.crypto.*;
import javax.crypto.spec.*;

public interface IPasswordManager {

    public void addUser(String userName, String publicSalt, String password, DataOutputStream out);

    public boolean authenticate(String userName, String password) throws FileNotFoundException, NoSuchAlgorithmException, IOException, InvalidKeyException, IllegalBlockSizeException, NoSuchPaddingException, BadPaddingException, InvalidAlgorithmParameterException;

    public void generateEncryptedFile(ByteArrayOutputStream byteStream);

}
