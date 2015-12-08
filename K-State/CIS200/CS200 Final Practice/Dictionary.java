public class Dictionary{
		private String[] words;
	
		public Dictionary(String[] s){
			words = new String[s.length];
			for(int i = 0; i<s.length;i++){
				words[i] = s[i];
			}
		}
		
	
		public boolean containWord(String s){
			for(int i=0;i<words.length;i++){
				if(s.equals(words[i]))
					return true;
			}
			return false;
		}
		
		public int startsWith(char c){
			int count = 0;
			for(int i=0;i<words.length;i++){
				if(c == words[i].charAt(0))
					count++;
			}
			return count;
		}
		
		public static int indexOf(String[] w, String s){
			for(int i =0; i<w.length; i++){
				if(s.equals(w[i]))
					return i;
		}
		throw new IllegalArgumentException();
	}
	
}
