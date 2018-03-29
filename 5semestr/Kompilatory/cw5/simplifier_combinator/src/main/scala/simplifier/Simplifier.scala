package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = {
    node match {
      case NodeList(list) =>
        val newList = list.map(simplify).filter(_ != EmptyNode)

        val pairs = newList.dropRight(1).zip(newList.drop(1))
        val assignmentsToDelete = pairs.collect{
          case (x@Assignment(var1,_),Assignment(var2,_)) if var1 == var2 =>
            x
        }

        newList.diff(assignmentsToDelete) match {
          case List() =>
            EmptyNode
          case List(NodeList(nestedList))=>
            NodeList(nestedList)
          case justList =>
            NodeList(justList)
        }

      case unary:Unary=>
        simplifyUnary(unary)
      case expr:BinExpr=>
        simplifyBin(expr)


      case Assignment(a,b) if a == simplify(b) =>
        EmptyNode
      case Assignment(a,b) =>
        Assignment(a,simplify(b))
      case WhileInstr(cond,body) if simplify(cond) == FalseConst =>
        EmptyNode
      case KeyDatumList(list)=>
        KeyDatumList(list.groupBy(_.key).map{case(key,values)=>values.last}.toList)
      case IfInstr(cond,left) if simplify(cond) == FalseConst  =>
        EmptyNode
      case IfElseInstr(cond,left,_) if simplify(cond) == TrueConst  =>
        simplify(left)
      case IfElseInstr(cond,_,right) if simplify(cond) == FalseConst =>
        simplify(right)
      case IfElseExpr(cond,left,_) if simplify(cond) == TrueConst  =>
        simplify(left)
      case IfElseExpr(cond,_,right) if simplify(cond) == FalseConst =>
        simplify(right)
      case node =>
        node
    }
  }

  def simplifyUnary(unary:Unary)={

    val helpOperatorMap = Map(
      "==" -> "!=",
      "!=" -> "==",
      "<=" -> ">",
      "<" -> ">=",
      ">=" -> "<",
      ">" -> "<="
    )

    (unary.op,simplify(unary.expr)) match {
      case ("-",Unary("-",node)) => node
      case ("not",Unary("not",node)) => node
      case ("not",TrueConst) => FalseConst
      case ("not",FalseConst) => TrueConst
      case ("not",BinExpr(op,left,right)) if helpOperatorMap.contains(op) =>
        BinExpr(helpOperatorMap(op),left,right)
      case ("-",FloatNum(x)) => FloatNum(-x)
      case ("-",IntNum(x)) => IntNum(-x)
      case (op,node) => Unary(op,node)
    }
  }


  def simplifyBin(expr:BinExpr):Node={

    val expr2 = BinExpr(expr.op,simplify(expr.left),simplify(expr.right))
    expr2 match {
      case BinExpr("+",leftOther, rightOther) if isZero(leftOther)  => rightOther
      case BinExpr("+",leftOther, rightOther) if isZero(rightOther)  => leftOther
      case BinExpr("-",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => IntNum(0)
      case BinExpr("or",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => leftOther
      case BinExpr("==",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => TrueConst
      case BinExpr("<=",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => TrueConst
      case BinExpr(">=",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => TrueConst
      case BinExpr("!=",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => FalseConst
      case BinExpr("<",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => FalseConst
      case BinExpr(">",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => FalseConst
      case BinExpr("and",leftOther, rightOther) if leftOther.EqualsCus(rightOther)  => leftOther
      case BinExpr("and",leftOther, rightOther) if leftOther.EqualsCus(FalseConst) || rightOther.EqualsCus(FalseConst)  => FalseConst
      case BinExpr("and",leftOther, rightOther) if leftOther.EqualsCus(TrueConst)  => rightOther
      case BinExpr("and",leftOther, rightOther) if rightOther.EqualsCus(TrueConst)  => leftOther
      case BinExpr("or",leftOther, rightOther) if leftOther.EqualsCus(TrueConst) || rightOther.EqualsCus(TrueConst) => TrueConst
      case BinExpr("or",leftOther, rightOther) if rightOther.EqualsCus(FalseConst)  => leftOther
      case BinExpr("or",leftOther, rightOther) if leftOther.EqualsCus(TrueConst)  => rightOther
      case x @ BinExpr(op,leftOther, rightOther) if evaluateConstants.isDefinedAt(x) => evaluateConstants(x)
      case x @ BinExpr(op,leftOther, rightOther) if simplifyBinUna.isDefinedAt(x) => simplifyBinUna(x)
      case x @ BinExpr(op,leftOther, rightOther) if simplifyMultip.isDefinedAt(x) => simplifyMultip(x)
      case x @ BinExpr(op,leftOther, rightOther) if simplifyDivisionAndOthers.isDefinedAt(x) => simplifyDivisionAndOthers(x)
      case x @ BinExpr(op,leftOther, rightOther) if simplifyConcat.isDefinedAt(x) => simplifyConcat(x)
      case x @ BinExpr(op,leftOther, rightOther) if simplifyPower.isDefinedAt(x) => simplifyPower(x)
      case _ => expr2

    }

  }

  val simplifyPower: PartialFunction[BinExpr,Node] ={
    case BinExpr("**",a,IntNum(0)) =>
      IntNum(1)
    case BinExpr("**",a,IntNum(1)) =>
      a
    case BinExpr("**",IntNum(1),a) =>
      IntNum(1)
    case BinExpr("*",BinExpr("**",a,b),BinExpr("**",c,d)) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("**",a,BinExpr("+",b,d)))
    case BinExpr("**",BinExpr("**",a,b),c) =>
      BinExpr("**",a,BinExpr("*",b,c))
    case BinExpr("+",
          BinExpr("+",
            BinExpr("**",a,IntNum(2)),
            BinExpr("*",BinExpr("*",IntNum(2),b),c)
          ),
          BinExpr("**",d,IntNum(2))
          ) if a.EqualsCus(b) && c.EqualsCus(d) =>
      BinExpr("**",BinExpr("+",a,c),IntNum(2))
    case BinExpr("-",
            BinExpr("-",
              BinExpr("**",BinExpr("+",a,b),IntNum(2)),
              BinExpr("**",c,IntNum(2))
            ),
            BinExpr("*",BinExpr("*",IntNum(2),d),e)
         ) if a.EqualsCus(c) && c.EqualsCus(d) && b.EqualsCus(e)=>
            BinExpr("**",b,IntNum(2))
    case BinExpr("-",
          BinExpr("**",BinExpr("+",a,b),IntNum(2)),
          BinExpr("**",BinExpr("-",c,d),IntNum(2))
         ) if a.EqualsCus(c) && b.EqualsCus(d) =>
      BinExpr("*",BinExpr("*",IntNum(4),a),b)
  }

  val simplifyMultip: PartialFunction[BinExpr,Node] ={

    case BinExpr("*",a, b) if isOne(a)  => b
    case BinExpr("*",a, b) if isOne(b)  => a
    case BinExpr("*",a, b) if isZero(a) || isZero(b) => IntNum(0)

    case BinExpr("-",BinExpr("*",a,b),c) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("*",a,BinExpr("-",b,IntNum(1))))

    case BinExpr("-",c,BinExpr("*",a,b)) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("*",a,BinExpr("-",IntNum(1),b)))

    case BinExpr("-",BinExpr("*",b,a),c) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("*",a,BinExpr("-",b,IntNum(1))))

    case BinExpr("-",c,BinExpr("*",b,a)) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("*",a,BinExpr("-",IntNum(1),b)))

    case BinExpr("+",BinExpr("*",a,b),BinExpr("*",c,d)) if a.EqualsCus(c)=>
      simplifyBin(BinExpr("*",a,BinExpr("+",b,d)))
    case BinExpr("+",BinExpr("*",a,b),BinExpr("*",c,d)) if a.EqualsCus(d)=>
      simplifyBin(BinExpr("*",a,BinExpr("+",b,c)))
    case BinExpr("+",BinExpr("*",a,b),BinExpr("*",c,d)) if b.EqualsCus(c)=>
      simplifyBin(BinExpr("*",BinExpr("+",a,d),b))

    case BinExpr("+",BinExpr("*",a,b),BinExpr("*",c,d)) if b.EqualsCus(d)=>
      simplifyBin(BinExpr("*",BinExpr("+",a,c),b))

    case BinExpr("+",
    BinExpr("+",
      BinExpr("*",a,BinExpr("+",b,c)),
        BinExpr("*",d,e)
      ),
      BinExpr("*",f,g)
    )
      if b.EqualsCus(e) && c.EqualsCus(g) && d.EqualsCus(f) =>

      BinExpr("*",BinExpr("+",a,d),BinExpr("+",b,c))

  }

  val evaluateConstants: PartialFunction[BinExpr,Node] ={
      case BinExpr(op,leftNum:FloatNum,rightNum:FloatNum)=>
        FloatNum(executeDoubleBin(op,leftNum.value,rightNum.value))
      case BinExpr(op,leftNum:IntNum,rightNum:FloatNum)=>
        FloatNum(executeDoubleBin(op,leftNum.value.toDouble,rightNum.value))
      case BinExpr(op,leftNum:FloatNum,rightNum:IntNum)=>
        FloatNum(executeDoubleBin(op,leftNum.value,rightNum.value.toDouble))
      case BinExpr(op,leftNum:IntNum,rightNum:IntNum)=>
        IntNum(executeIntBin(op,leftNum.value,rightNum.value))
  }

  val simplifyDivisionAndOthers: PartialFunction[BinExpr,Node]={

    case BinExpr("/",a, b) if a.EqualsCus(b)  => IntNum(1)
    case BinExpr("/",a, b) if isZero(a)  => IntNum(0)
    case BinExpr("/",a,BinExpr("/",b,c)) if isOne(a) && isOne(b) => c
    case BinExpr("/",BinExpr("/",b,c),a) if isOne(a) && isOne(b) => c

    case BinExpr("*",a,BinExpr("/",b,c)) if isOne(b) && isOne(b) => BinExpr("/",a,c)
    case BinExpr("*",BinExpr("/",b,c),a) if isOne(b) && isOne(b) => BinExpr("/",a,c)

    case BinExpr("+",a,BinExpr("-",b,c)) if a.EqualsCus(c) => b
    case BinExpr("+",BinExpr("-",b,c),a) if a.EqualsCus(c) => b

    case BinExpr("-",a,BinExpr("+",b,c)) if a.EqualsCus(b) => Unary("-",c)
    case BinExpr("-",a,BinExpr("+",b,c)) if a.EqualsCus(c) => Unary("-",b)

    case BinExpr("-",BinExpr("+",b,c),a) if a.EqualsCus(b) => c
    case BinExpr("-",BinExpr("+",b,c),a) if a.EqualsCus(c) => b
  }


  val simplifyBinUna: PartialFunction[BinExpr,Node] ={

      case BinExpr("+",Unary("-",leftNode),Unary("-",rightNode))  =>
        Unary("-",BinExpr("+",leftNode,rightNode))

      case BinExpr("+",Unary("-",leftNode),rightNode)  =>
        simplifyBin(BinExpr("-",rightNode,leftNode))

      case BinExpr("+",leftNode,Unary("-",rightNode))  =>
        simplifyBin(BinExpr("-",leftNode,rightNode))

  }

  val simplifyConcat: PartialFunction[BinExpr,Node] ={
    case BinExpr("+",ElemList(list1),ElemList(list2))  =>
      ElemList(list1++list2)
    case BinExpr("+",Tuple(list1),Tuple(list2))  =>
      Tuple(list1++list2)
  }


  def isZero(node:Node)={
    node match {
      case IntNum(0) => true
      case FloatNum(0.0) => true
      case _ => false
    }
  }

  def isOne(node:Node)={
    node match {
      case IntNum(1) => true
      case FloatNum(1.0) => true
      case _ => false
    }
  }

  def executeIntBin(op:String, left:Int, right:Int):Int={
    op match {
      case "**" => math.pow(left,right).toInt
      case "*" => left * right
      case "/" => left / right
      case "+" => left + right
      case "-" => left - right
    }
  }

  def executeDoubleBin(op:String, left:Double, right:Double):Double={
    op match {
      case "**" => math.pow(left,right)
      case "*" => left * right
      case "/" => left / right
      case "+" => left + right
      case "-" => left - right
    }
  }

}
