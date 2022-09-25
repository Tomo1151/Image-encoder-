import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.Math;
import javax.imageio.ImageIO;
import java.lang.Exception;

public class ShearMap {
	public static final int COLOR_SIZE = 256; 

	public static void main(String[] args) {
		long startTime = System.currentTimeMillis();

		int picWidth;
		int picHeight;
		FileOutputStream fos;
		BufferedImage image;
		BufferedImage imageC;
		BufferedImage imageRG;
		BufferedImage transedImage;
		BufferedImage transedImageRG;
		BufferedImage transedImageRB;
		BufferedImage transedImageGB;
		int[][] mapRG = new int[COLOR_SIZE][COLOR_SIZE];
		int[][] mapRB = new int[COLOR_SIZE][COLOR_SIZE];
		int[][] mapGB = new int[COLOR_SIZE][COLOR_SIZE];

		try{
			image = ImageIO.read(new File("img/" + args[0] + ".png"));
			fos = new FileOutputStream("LZ/temp/shear.data");
		}catch(IOException e){
			image = null;
			System.out.println(e);
			fos = null;
		}

		picWidth = image.getWidth();
		picHeight = image.getHeight();

		for(int i = 0; i < COLOR_SIZE; i++){
			for(int j = 0; j < COLOR_SIZE; j++){
				mapRG[i][j] = 0;
				mapRB[i][j] = 0;
				mapGB[i][j] = 0;
			}
		}

		imageC = new BufferedImage(picWidth, picHeight, BufferedImage.TYPE_INT_RGB);
		for(int i = 0; i < picHeight; i++){
			for(int j = 0; j < picWidth; j++){
				int c = (image.getRGB(i, j) + 256*256*256) % (256*256*256);
				int r = c/65536;
				int g = (c/256)%256;
				int b = c % 256;
				imageC.setRGB(i, j, r*65536 + g*256 + b);
			}
		}
		
		
		{
			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (image.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					mapRG[r][g]++;
				}
			}

			imageRG = new BufferedImage(COLOR_SIZE, COLOR_SIZE, BufferedImage.TYPE_INT_RGB);

			int maxRmG = 0;
			int minRmG = 255;
			for(int i = 0; i < COLOR_SIZE; i++){
				for(int j = 0; j < COLOR_SIZE; j++){
					if(mapRG[i][j] != 0){
						if(j - i > maxRmG){
							maxRmG = j - i;
						}
						if(j - i < minRmG){
							minRmG = j - i;
						}
					}
				}
			}

			try{
				fos.write(minRmG * -1);
			}catch(IOException e){
				System.out.println(e);
			}


			for(int i = 0; i < COLOR_SIZE; i++){
				for(int j = 0; j < COLOR_SIZE; j++){
					imageRG.setRGB(i, j, mapRG[i][j] == 0 ? 0 : 0xffffff);
				}
			}
			for(int i = 0; i < COLOR_SIZE; i++){
				if(0 <= i + maxRmG && i + maxRmG < COLOR_SIZE){
					imageRG.setRGB(i, i + maxRmG, 0x00ffff);
				}
				if(0 <= i + minRmG && i + minRmG < COLOR_SIZE){
					imageRG.setRGB(i, i + minRmG, 0x00ff00);
				}
			}

			transedImage = new BufferedImage(picWidth, picHeight, BufferedImage.TYPE_INT_RGB);
			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (image.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					transedImage.setRGB(i, j, 65536*r + 256*(g - r - minRmG) + b);
				}
			}
		}


		{
			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (transedImage.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					mapRB[r][b]++;
				}
			}

			int maxRmG = 0;
			int minRmG = 255;
			for(int i = 0; i < COLOR_SIZE; i++){
				for(int j = 0; j < COLOR_SIZE; j++){
					if(mapRB[i][j] != 0){
						if(j - i > maxRmG){
							maxRmG = j - i;
						}
						if(j - i < minRmG){
							minRmG = j - i;
						}
					}
				}
			}

			try{
				fos.write(minRmG * -1);
			}catch(IOException e){
				System.out.println(e);
			}

			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (transedImage.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					transedImage.setRGB(i, j, 65536*r + 256*g + (b - r - minRmG));
				}
			}
		}


		{
			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (transedImage.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					mapGB[g][b]++;
				}
			}

			int maxRmG = 0;
			int minRmG = 255;
			for(int i = 0; i < COLOR_SIZE; i++){
				for(int j = 0; j < COLOR_SIZE; j++){
					if(mapGB[i][j] != 0){
						if(j - i > maxRmG){
							maxRmG = j - i;
						}
						if(j - i < minRmG){
							minRmG = j - i;
						}
					}
				}
			}

			try{
				fos.write(minRmG * -1);
			}catch(IOException e){
				System.out.println(e);
			}

			for(int i = 0; i < picHeight; i++){
				for(int j = 0; j < picWidth; j++){
					int c = (transedImage.getRGB(i, j) + 256*256*256) % (256*256*256);
					int r = c/65536;
					int g = (c/256)%256;
					int b = c % 256;
					transedImage.setRGB(i, j, 65536*r + 256*g + (b - g - minRmG));
				}
			}
		}


		transedImageRG = new BufferedImage(COLOR_SIZE, COLOR_SIZE, BufferedImage.TYPE_INT_RGB);
		for(int i = 0; i < COLOR_SIZE; i++){
			for(int j = 0; j < COLOR_SIZE; j++){
				int c = (transedImage.getRGB(i, j) + 256*256*256) % (256*256*256);
				int r = c/65536;
				int g = (c/256)%256;
				int b = c % 256;
				transedImageRG.setRGB(g, b, 0xffffff);
			}
		}

		try{
			fos.flush();
			fos.close();
		}catch(IOException e){
			System.out.println(e);
		}

		try{
			ImageIO.write(transedImage, "png", new File("LZ/temp/sheared.data"));
		}catch(Exception e){
			System.out.println(e);
		}
		// long endTime = System.currentTimeMillis();

		// System.out.println((endTime - startTime) / 1000.0 + " sec");
	}
}
