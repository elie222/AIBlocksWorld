package blocksWorld.gui;


import java.awt.*;
import java.util.ArrayList;
import java.util.Collection;
import javax.swing.JTextArea;

public class Game extends java.applet.Applet {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private int mouseX, mouseY;
	private boolean mouseclicked = false;
	private Collection<BoxG> bCol = new ArrayList<BoxG>();
	private int distX = BoxG.width/2;
	private int distY = BoxG.hight/2;
	private BoxG drag;
	private String dragOn;
	Collection<String> facts = new ArrayList<String>();
	private char cha = 'A';
        JTextArea TextArea;
	
	public void init()  {
		bCol.add(new BoxG('A',0,0));
		facts.add("A ON TABLE");
		setBackground(Color.BLACK);
		setSize(200,400);
		repaint();
	}
	
	public boolean mouseDrag(Event evt, int x, int y){
		mouseX=x; mouseY=y;
		change();
		return true;
	}
	
	public boolean mouseUp(Event evt,int x,int y){
		mouseclicked = false;
		deleteRelated();
		if(dragOn == null)
			facts.add(drag.getName() + " ON TABLE");
		else facts.add(dragOn);
		BoxG w = checkAbove();
		if(w != null){
			facts.add(w.getName() + " ON " + drag.getName());
			facts.remove(w.getName() + " ON TABLE");
		}
                TextArea.setText(MyToString());
		return true;
	}
	
	private BoxG checkAbove() {
		for(BoxG b : bCol)
			if(b.getX() == drag.getX() && b.getY() + BoxG.hight + 1 == drag.getY())
				return b;
		return null;
	}

	public void change(){
		if(!mouseclicked){
			for(BoxG b : bCol){
				if(b.isInside(mouseX, mouseY)){
					mouseclicked = true;
					drag = b;
					distX = mouseX - b.getX();
					distY = mouseY - b.getY();
					break;
				}
			}
		}
		else{
			drag.setX(mouseX - distX);
			drag.setY(mouseY - distY);
			dragOn = null;
			for(BoxG d : bCol){
				if(drag.equals(d))
					continue;
				if(drag.isCrash(d)){
					drag.repair(d);
					dragOn = drag.getName() + " ON " + d.getName();
					repaint();
					doAgain();
					return;
				}
			}
		}
		repaint();
	}
	
	private void deleteRelated() {
		Collection<String> remove = new ArrayList<String>();
		Collection<String> add = new ArrayList<String>();
                if(drag == null)
                    return;
		for(String s : facts){
			if(s.matches(drag.getName() + " ON ."))
				remove.add(s);
			if(s.matches(". ON " + drag.getName())){
				remove.add(s);
				add.add(s.charAt(0) + " ON TABLE");	
			}
			if(s.matches(drag.getName() + " ON TABLE"))
				remove.add(s);
		}
		for(String s: remove)
			facts.remove(s);
		for(String s: add)
			facts.add(s);
	}

	public void doAgain(){
		for(BoxG d : bCol){
			if(drag.equals(d))
				continue;
			if(drag.isCrash(d)){
				drag.repair(d);
				repaint();
				dragOn = drag.getName() + " ON " + d.getName();
				doAgain();
				return;
			}
		}
	}
	
	/*public boolean mouseDown(Event e, int x, int y ) {
		mouseX=x; mouseY=y;
		mouseclicked = true;
		repaint();
		return true;
	}*/
	
	public void paint(Graphics g) {
		for(BoxG b : bCol)
			paintBox(g, b);
	}    
	
	public void paintBox(Graphics g, BoxG b){
		g.setColor(Color.WHITE);
		g.fillRect(b.getX(), b.getY(), BoxG.width, BoxG.hight);
		g.setColor(Color.BLACK);
		g.drawChars(b.getNameByArray(), 0, 1, b.getX()+8, b.getY()+16);
	}
	
	public void addCube(){
		bCol.add(new BoxG(++cha,0,0));
		facts.add(cha + " ON TABLE");
		repaint();
                TextArea.setText(MyToString());
	}
	
	public String toString(){
		String s = "";
		for(String f : facts)
			s += f + ",";
		s = s.substring(0 , s.length() - 1);
		return s;
	}
	
	public String getBoxes(){
		String s = "";
		for(BoxG b : bCol)
			s += "BOX:" + b.getName() + ",";
		s = s.substring(0 , s.length() - 1);
		return s;
	}

	public String MyToString(){
		String s = "";
		for(String f : facts)
			s += f + "\n";
		s = s.substring(0 , s.length() - 1);
		return s;
	}

    public void addWritingComponent(JTextArea jTextArea1) {
       TextArea = jTextArea1;
       TextArea.setText(MyToString());
    }
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	 /*public void update ( Graphics g ) {
		 paint(g);
	 }*/

	 /*void GetImages () {
		 // Get images for cards1 and 2
		 // Get image for card3 if it is needed
		 
		 card1 = getImage(getCodeBase(), "src\\picture4.png");
		 //Image card2 = getImage(getCodeBase(), "");
		 
		 /*Image card3;
		 if (game.card3_file != null)
			 card3 = getImage(getCodeBase(), "cards/"+game.deck.card3_file);
	}*/

	 
}

