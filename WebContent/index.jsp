
<%@ include file="inc/header.jsp" %>
<form method="post" action="sms-exec.jsp" style="margin:0px; padding:0px;">
    <table>
    <tr>
    <td>
    Number:
    </td>
    <td>
    <input type="text" name="number" value="" />
    </td>
    </tr>
    <tr>
    <td>
    Text:
    </td>
    <td>
    <textarea name="text"></textarea>
	</td>
	</tr>
	<tr>
    <td>
    Delay:
    </td>
    <td>
	<select name="delay">
	<option value="0" selected="true">No Delay</option>
	<option value="1">1 minute</option>
	<option value="5">5 minutes</option>
	<option value="10">10 minutes</option>
	<option value="15">15 minutes</option>
	<option value="30">30 minutes</option>
	<option value="45">45 minutes</option>
	<option value="60">1 hour</option>
	<option value="120">2 hours</option>
	<option value="300">5 hours</option>
	</select>
	</td>
	</tr>
	<tr>
	<td>
    <input type="submit" value="Send Message"/>
    </td>
    </tr>
    </table>     
</form>

<%@ include file="inc/footer.jsp" %>
