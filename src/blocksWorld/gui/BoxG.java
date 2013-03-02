package blocksWorld.gui;


public class BoxG {
	public static final int width = 25;
	public static final int hight = 25;
	private char name;
	private int x;
	private int y;
	
	public BoxG(char c, int x, int y){
		this.name = c;
		this.x = x;
		this.y = y;
	}
	
	public void setName(char name) {
		this.name = name;
	}
	public char getName() {
		return name;
	}
	public void setX(int x) {
		this.x = x;
	}
	public int getX() {
		return x;
	}
	public void setY(int y) {
		this.y = y;
	}
	public int getY() {
		return y;
	}
	
	public char[] getNameByArray(){
		char[] a = {name};
		return a;
	}
	
	public boolean isInside(int xNow, int yNow){
		if(xNow >= x && xNow <= x+width && yNow >= y && yNow <= y+hight)
			return true;
		return false;
	}
	
	public boolean isCrash(BoxG b){
		return isInside(b.getX(), b.getY()) || isInside(b.getX() + width, b.getY()) ||
		isInside(b.getX(), b.getY() + hight) || isInside(b.getX() + width, b.getY() + hight);
	}
	
	public boolean equals(BoxG b){
		return x == b.getX() && y == b.getY() && name == b.getName();
	}
	
	public void repair(BoxG b){
		x = b.getX();
		y = b.getY() - hight - 1;
	}
}
