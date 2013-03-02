package blocksWorld;

public class Box implements Comparable<Box>{

	private String _name;
	
	public Box(String name){
		_name = name;
	}
	
	public String toString(){
		return _name;
	}
	
	public boolean equals(Object b){
		if(b instanceof Box)
			return ((Box)b)._name.equals(_name);
		return false;
	}
	
	@Override
	public int compareTo(Box o) {
		return o._name.compareTo(_name);
	}

	public Box dup() {
		return new Box(new String(_name));
	}
	
	public void setName(String s) {
		_name = s;
	}

}
